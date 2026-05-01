from mpi4py import MPI
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


def generate_orders():
    return [
        {"order_id": 1, "item": "Laptop"},
        {"order_id": 2, "item": "Mouse"},
        {"order_id": 3, "item": "Keyboard"},
        {"order_id": 4, "item": "Monitor"},
        {"order_id": 5, "item": "Headphones"},
        {"order_id": 6, "item": "USB Cable"},
    ]


def assign_orders_to_workers(orders):
    worker_count = size - 1
    assignments = [[] for _ in range(worker_count)]

    for index, order in enumerate(orders):
        worker_index = index % worker_count
        assignments[worker_index].append(order)

    return assignments


def main():
    if size < 2:
        if rank == 0:
            print("Run this program with at least 2 processes: 1 master + 1 worker.")
        return

    if rank == 0:
        orders = generate_orders()
        assignments = assign_orders_to_workers(orders)

        print("[MASTER] Generated orders:")
        for order in orders:
            print(f"  Order {order['order_id']}: {order['item']}")

        for worker_rank in range(1, size):
            comm.send(assignments[worker_rank - 1], dest=worker_rank, tag=11)
            print(f"[MASTER] Sent {len(assignments[worker_rank - 1])} order(s) to worker {worker_rank}")

        completed_orders = []
        for _ in range(1, size):
            worker_results = comm.recv(source=MPI.ANY_SOURCE, tag=22)
            completed_orders.extend(worker_results)

        print("\n[MASTER] Completed orders:")
        for order in completed_orders:
            print(
                f"  Order {order['order_id']} ({order['item']}) handled by worker {order['handled_by']}"
            )
    else:
        my_orders = comm.recv(source=0, tag=11)
        print(f"[WORKER {rank}] Received order(s): {[order['order_id'] for order in my_orders]}")

        processed_orders = []
        for order in my_orders:
            time.sleep(1)
            print(f"[WORKER {rank}] Processed order {order['order_id']}: {order['item']}")
            processed_orders.append(
                {
                    "order_id": order["order_id"],
                    "item": order["item"],
                    "handled_by": rank,
                }
            )

        comm.send(processed_orders, dest=0, tag=22)


if __name__ == "__main__":
    main()
