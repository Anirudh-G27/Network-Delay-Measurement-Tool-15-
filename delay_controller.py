from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class DelayController(object):
    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        dpid = event.dpid
        in_port = event.port

        # 1. Handle ARP by flooding so hosts can find each other's MAC addresses
        if packet.type == packet.ARP_TYPE:
            msg = of.ofp_packet_out()
            msg.data = event.ofp
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            self.connection.send(msg)
            return

        # 2. Handle IP Traffic and install explicit flow rules based on ToS
        if packet.type == packet.IP_TYPE:
            ip_packet = packet.payload
            tos = ip_packet.tos

            # Create an OpenFlow flow modification message
            msg = of.ofp_flow_mod()
            # Match the exact flow of this packet (including the ToS field)
            msg.match = of.ofp_match.from_packet(packet, in_port)
            msg.idle_timeout = 30 # Rule expires after 30 seconds of inactivity

            # Routing Logic based on Switch DPID
            if dpid == 1: # Switch 1 (Ingress from h1)
                if in_port == 1: 
                    # Packet coming from h1, decide path based on ToS
                    if tos == 4:
                        log.info("S1: Routing ToS 4 via FAST PATH (s2)")
                        msg.actions.append(of.ofp_action_output(port=2))
                    elif tos == 8:
                        log.info("S1: Routing ToS 8 via SLOW PATH (s3)")
                        msg.actions.append(of.ofp_action_output(port=3))
                    else:
                        msg.actions.append(of.ofp_action_output(port=2)) # Default to fast
                else: 
                    # Returning traffic from s2 or s3 goes back to h1
                    msg.actions.append(of.ofp_action_output(port=1))

            elif dpid == 4: # Switch 4 (Ingress from h2)
                if in_port == 3: 
                    # Packet coming from h2, send back via the same path based on ToS
                    if tos == 4:
                        msg.actions.append(of.ofp_action_output(port=1)) # via s2
                    elif tos == 8:
                        msg.actions.append(of.ofp_action_output(port=2)) # via s3
                    else:
                        msg.actions.append(of.ofp_action_output(port=1)) # Default
                else:
                    # Traffic from s2 or s3 goes to h2
                    msg.actions.append(of.ofp_action_output(port=3))

            elif dpid == 2 or dpid == 3: # Intermediate Switches (s2 and s3)
                # Simple pass-through: if it comes in port 1, go out 2, and vice versa
                out_port = 2 if in_port == 1 else 1
                msg.actions.append(of.ofp_action_output(port=out_port))

            # Send the flow rule to the switch
            self.connection.send(msg)

            # Also forward the current packet that triggered the PacketIn
            packet_out = of.ofp_packet_out()
            packet_out.data = event.ofp
            packet_out.actions = msg.actions
            self.connection.send(packet_out)

def launch():
    def start_switch(event):
        log.info("Controller attached to Switch %s" % (event.connection.dpid,))
        DelayController(event.connection)
    core.openflow.addListenerByName("ConnectionUp", start_switch)