from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ethernet, ipv4, arp

log = core.getLogger()

# Allowed communication (only define one direction)
whitelist = [
    ("10.0.0.1", "10.0.0.2"),
    ("10.0.0.2", "10.0.0.3")
]

# MAC learning table
mac_to_port = {}

def _handle_ConnectionUp(event):
    log.info("Switch connected!")

def _handle_PacketIn(event):
    packet = event.parsed
    in_port = event.port

    if not packet:
        return

    # Learn MAC address
    mac_to_port[packet.src] = in_port

    # Allow ARP (important for ping to work)
    if packet.find('arp'):
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)
        return

    ip_packet = packet.find('ipv4')
    if not ip_packet:
        return

    src_ip = str(ip_packet.srcip)
    dst_ip = str(ip_packet.dstip)

    log.info(f"Packet: {src_ip} -> {dst_ip}")

    # Decide output port using MAC learning
    if packet.dst in mac_to_port:
        out_port = mac_to_port[packet.dst]
    else:
        out_port = of.OFPP_FLOOD

    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet, in_port)

    # Bidirectional check (CRITICAL FIX)
    if (src_ip, dst_ip) in whitelist or (dst_ip, src_ip) in whitelist:
        log.info(f"ALLOWED: {src_ip} -> {dst_ip}")

        # Install forwarding rule
        msg.actions.append(of.ofp_action_output(port=out_port))
        event.connection.send(msg)

        # Send current packet
        packet_out = of.ofp_packet_out()
        packet_out.data = event.ofp
        packet_out.actions.append(of.ofp_action_output(port=out_port))
        event.connection.send(packet_out)

    else:
        log.info(f"BLOCKED: {src_ip} -> {dst_ip}")
        # Drop rule (no actions)
        event.connection.send(msg)

def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
