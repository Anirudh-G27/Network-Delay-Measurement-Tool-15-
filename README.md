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
sudo mn --custom delay_topo.py --topo delaytopo --mac --controller=remote --link tc
```

## 3. Expected Output
The custom topology consists of two paths between Host 1 (h1) and Host 2 (h2):

Fast Path (via switch s2): Links are configured with a 5ms delay.

Slow Path (via switch s3): Links are configured with a 50ms delay.

When testing connectivity using the ping command with the -Q (ToS) flag:

h1 ping -c 4 -Q 4 h2: The controller will route this via the Fast Path. The expected Round Trip Time (RTT) is approximately ~20-25ms.

h1 ping -c 4 -Q 8 h2: The controller will route this via the Slow Path. The expected RTT is approximately ~200-205ms.


## 4. Proof of Execution

* Ping results
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3f7d5f34-ae4b-4f43-b283-902528ab0e00" />

<br>

* Flow Table
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/8fdaf547-513f-4b6b-835e-3eb56637c847" />

<br>

* Fast Path Verification (ToS = 4)
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/72f448e5-0acb-443c-a2ca-42812683a5d2" />

<br>

* Slow Path Verification (ToS = 8)
<img width="1920" height="1080" alt="Screenshot 2026-04-19 204100" src="https://github.com/user-attachments/assets/744c238d-24fd-4726-a03d-0c90b6c3f5c5" />
