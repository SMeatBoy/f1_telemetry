import asyncio
import datetime
import random
import socket
import json

import websockets

from ctypes_json import CDataJSONEncoder

from f1_2019_struct import *


def telemetry():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 27077))

    while True:
        data, addr = sock.recvfrom(5000)
        # print("received! Packet")
        packet_header = PacketHeader.from_buffer_copy(data[0:23])
        # print(packet_header.m_packetId)
        if int(packet_header.m_packetId) == 0:
            # print("Motion Packet")
            # car_motion_data = PacketMotionData.from_buffer_copy(data[0:1343])
            pass
        elif int(packet_header.m_packetId) == 1:
            # print("Session Packet")
            packet_session_data = PacketSessionData.from_buffer_copy(data[0:149])
        elif int(packet_header.m_packetId) == 2:
            # print("Lap Data Packet")
            packet_lap_data = PacketLapData.from_buffer_copy(data[0:843])
            lap_data = packet_lap_data.m_lapData
            print("Distance Car 0: ", lap_data[0].m_totalDistance)
        elif int(packet_header.m_packetId) == 3:
            pass
            # print("Event Packet")
        elif int(packet_header.m_packetId) == 4:
            pass
            # print("Participants Packet")
        elif int(packet_header.m_packetId) == 5:
            pass
            # print("Car Setups Packet")
        elif int(packet_header.m_packetId) == 6:
            pass
            # print("Car Telemetry Packet")
            # packet_car_telemetry_data = PacketCarTelemetryData.from_buffer_copy(data[0:1347])
            # car_0_telemetry_data = packet_car_telemetry_data.m_carTelemetryData[0]
            # print("\tVelocity: ", car_0_telemetry_data.m_speed)
        elif int(packet_header.m_packetId) == 7:
            pass
            # print("Car Status Packet")


def udp_packet_to_json(data):
    packet = ""
    packet_header = PacketHeader.from_buffer_copy(data[0:23])
    print(packet_header.m_packetId)
    if int(packet_header.m_packetId) == 0:
        packet = PacketMotionData.from_buffer_copy(data[0:1343])
    elif int(packet_header.m_packetId) == 1:
        packet = PacketSessionData.from_buffer_copy(data[0:149])
    elif int(packet_header.m_packetId) == 2:
        packet = PacketLapData.from_buffer_copy(data[0:843])
    elif int(packet_header.m_packetId) == 3:
        packet = PacketEventData.from_buffer_copy(data[0:32])
    elif int(packet_header.m_packetId) == 4:
        packet = PacketParticipantsData.from_buffer_copy(data[0:1104])
        print("Number of Cars: ",packet.m_numCars)
        json.dumps(packet.m_participants[0], cls=CDataJSONEncoder)
    elif int(packet_header.m_packetId) == 5:
        packet = PacketCarSetupData.from_buffer_copy(data[0:843])
    elif int(packet_header.m_packetId) == 6:
        packet = PacketCarTelemetryData.from_buffer_copy(data[0:1347])
    elif int(packet_header.m_packetId) == 7:
        packet = PacketCarStatusData.from_buffer_copy(data[0:1143])
    return json.dumps(packet, cls=CDataJSONEncoder)


def async_lap_distance():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 27077))

    async def producer():
        data, addr = sock.recvfrom(5000)
        packet_header = PacketHeader.from_buffer_copy(data[0:23])
        print(packet_header.m_packetId)
        while int(packet_header.m_packetId) != 2:
            pass
        packet_lap_data = PacketLapData.from_buffer_copy(data[0:843])
        lap_data = packet_lap_data.m_lapData
        distance = str(lap_data[0].m_totalDistance)
        return distance

    async def producer_handler(websocket, path):
        while True:
            message = await producer()
            await websocket.send(message)

    start_server = websockets.serve(producer_handler, "127.0.0.1", 5678)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def send_lap_distance():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 27077))

    async def total_distance(websocket, path):
        while True:
            data, addr = sock.recvfrom(1347)
            json_string = udp_packet_to_json(data)
            await websocket.send(json_string)

    start_server = websockets.serve(total_distance, "127.0.0.1", 5678)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def websocket_test():
    async def time(websocket, path):
        while True:
            now = datetime.datetime.utcnow().isoformat() + "Z"
            await websocket.send(now)
            await asyncio.sleep(random.random() * 3)

    start_server = websockets.serve(time, "127.0.0.1", 5678)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def main():
    # websocket_test()
    # telemetry()
    send_lap_distance()
    # async_lap_distance()


if __name__ == "__main__":
    main()
