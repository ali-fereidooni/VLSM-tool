import ipaddress
import math


def calculate_subnet(hosts_required):
    total_hosts = hosts_required + 2  # network + broadcast
    bits = math.ceil(math.log2(total_hosts))
    subnet_size = 2 ** bits
    wasted = subnet_size - total_hosts
    prefix = 32 - bits
    return subnet_size, prefix, wasted


def format_ip_range(network):
    all_hosts = list(network.hosts())
    if len(all_hosts) == 0:
        first = last = "N/A"
    elif len(all_hosts) == 1:
        first = last = str(all_hosts[0])
    else:
        first = str(all_hosts[0])
        last = str(all_hosts[-1])
    return first, last


def main():
    base_network_input = input("Enter base network (e.g., 192.168.1.0/24): ")
    base_network = ipaddress.ip_network(base_network_input, strict=False)

    room_types = int(input("Enter number of network types (e.g., 3): "))
    network_counts = list(map(int, input(
        f"Enter number of networks for each type (e.g., 1 3 3): ").split()))
    clients_required = list(
        map(int, input(f"Enter required hosts per type (e.g., 126 30 6): ").split()))

    if not (len(network_counts) == len(clients_required) == room_types):
        print("Input mismatch. Please try again.")
        return

    all_networks = []
    for i in range(room_types):
        for _ in range(network_counts[i]):
            all_networks.append(clients_required[i])

    # Sort by descending host requirements (VLSM standard)
    all_networks.sort(reverse=True)

    current_ip = base_network.network_address
    remaining_ips = base_network.num_addresses
    print("\n" + "="*90)
    print(f"{'Network Address':<20}{'Prefix':<10}{'Usable IPs':<25}{'Broadcast':<20}{'Wasted IPs'}")
    print("-"*90)

    for idx, host_count in enumerate(all_networks, start=1):
        subnet_size, prefix, wasted = calculate_subnet(host_count)
        try:
            subnet = ipaddress.ip_network(
                f"{current_ip}/{prefix}", strict=False)
        except ValueError:
            print(
                f"\n⚠ Out of IP range. No space for subnet requiring {host_count} hosts.")
            break

        first, last = format_ip_range(subnet)
        broadcast = str(subnet.broadcast_address)

        print(
            f"{str(subnet.network_address):<20}/{prefix:<8}{first} - {last:<18}{broadcast:<20}{wasted}")

        current_ip = subnet.broadcast_address + 1
        remaining_ips -= subnet.num_addresses

    print("="*90)
    print(f"Remaining unused IPs: {remaining_ips}")
    print("="*90)


if __name__ == "__main__":
    main()
