# SDN Mininet Simulation: Network Delay Measurement Tool (Orange Problem)

## 1. Problem Statement
The objective of this project is to implement an SDN-based solution using Mininet and the POX OpenFlow controller to measure and analyze network latency across different paths. 

The standard shortest-path routing is overridden by a custom SDN controller. The controller acts reactively to `packet_in` events by inspecting the IP Type of Service (ToS) field. Based on the ToS value, it installs explicit match-action flow rules to route traffic down either a "Fast Path" (low latency) or a "Slow Path" (high latency). This project demonstrates successful controller-switch interaction, OpenFlow rule design, and dynamic network behavior modification.

## 2. Setup and Execution Steps

### Prerequisites:
* Mininet network emulator installed.
* POX SDN controller installed.
* Custom scripts: `delay_topo.py` (Mininet topology) and `delay_controller.py` (POX controller).

### Execution:
This project requires running two separate terminal instances.

**Terminal 1: Start the POX Controller**
Navigate to the POX directory and start the custom controller. (Note: packet parsing warnings are suppressed to keep the output clean).
```bash
cd ~/pox
./pox.py log.level --DEBUG --packet=CRITICAL delay_controller
```

**Terminal 2: Launch the Mininet Topology**
Navigate to the directory containing the topology script and start Mininet, connecting it to the remote controller.
```bash
sudo mn -c
sudo mn --custom delay_topo.py --topo delaytopo --mac --controller=remote --link t
```

## 3. Expected Output
The custom topology consists of two paths between Host 1 (h1) and Host 2 (h2):

Fast Path (via switch s2): Links are configured with a 5ms delay.

Slow Path (via switch s3): Links are configured with a 50ms delay.

When testing connectivity using the ping command with the -Q (ToS) flag:

h1 ping -c 4 -Q 4 h2: The controller will route this via the Fast Path. The expected Round Trip Time (RTT) is approximately ~20-25ms.

h1 ping -c 4 -Q 8 h2: The controller will route this via the Slow Path. The expected RTT is approximately ~200-205ms.
