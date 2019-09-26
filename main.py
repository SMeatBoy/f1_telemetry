import socket
from f1_2019_struct import *

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 27077))

while True:
    data, addr = sock.recvfrom(5000)
    print("received! Packet")
    packet_header = PacketHeader.from_buffer_copy(data[0:23])
    print(packet_header.m_packetId)
    if int(packet_header.m_packetId) == 0:
        print("Motion Packet")
        car_motion_data = PacketMotionData.from_buffer_copy(data[0:1343])
    elif int(packet_header.m_packetId) == 1:
        print("Session Packet")
        packet_session_data = PacketSessionData.from_buffer_copy(data[0:149])
    elif int(packet_header.m_packetId) == 2:
        print("Lap Data Packet")
    elif int(packet_header.m_packetId) == 3:
        print("Event Packet")
    elif int(packet_header.m_packetId) == 4:
        print("Participants Packet")
    elif int(packet_header.m_packetId) == 5:
        print("Car Setups Packet")
    elif int(packet_header.m_packetId) == 6:
        print("Car Telemetry Packet")
        packet_car_telemetry_data = PacketCarTelemetryData.from_buffer_copy(data[0:1347])
        car_0_telemetry_data = packet_car_telemetry_data.m_carTelemetryData[0]
        print("\tVelocity: ", car_0_telemetry_data.m_speed)
    elif int(packet_header.m_packetId) == 7:
        print("Car Status Packet")
