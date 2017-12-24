import socket
from general import *
from networking.ethernet import Ethernet
from networking.ipv4 import IPv4
from networking.icmp import ICMP
from networking.tcp import TCP
from networking.udp import UDP
from networking.pcap import Pcap
from networking.http import HTTP
import time

TAB_1 = '\t - '
TAB_2 = '\t\t - '
TAB_3 = '\t\t\t - '
TAB_4 = '\t\t\t\t - '

DATA_TAB_1 = '\t   '
DATA_TAB_2 = '\t\t   '
DATA_TAB_3 = '\t\t\t   '
DATA_TAB_4 = '\t\t\t\t   '

#time,srcip,desip,,headerlength,protocol,hex,info,data 6,7,8 ...7,8,6
def main():

    pcap = Pcap('capture.pcap')
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    info =""
    Data=""
   # if StartCapture==1:
    Tstart=int(round(time.time() * 1000))
   #StartCapture=0
    while True:
        raw_data, addr = conn.recvfrom(65535)
        l=[]
        l.append(Tstart-int(round(time.time() * 1000)))

        pcap.write(raw_data)
        eth = Ethernet(raw_data)

        #print('\nEthernet Frame:')
        Data+="\nEthernet Frame:"+TAB_1 + "Destination:"+str(eth.dest_mac)+"Source: "+str(eth.src_mac)+"Protocol: "+str(eth.proto)
        #print(TAB_1 + 'Destination: {}, Source: {}, Protocol: {}'.format(eth.dest_mac, eth.src_mac, eth.proto))

        # IPv4
        if eth.proto == 8:
            ipv4 = IPv4(eth.data)
            Data += TAB_2 + 'Protocol: ' + str(ipv4.proto) + ' Source:' + str(ipv4.src) + 'Target:' + str(ipv4.target)
         #   print(TAB_2 + 'Protocol: {}, Source: {}, Target: {}'.format(ipv4.proto, ipv4.src, ipv4.target))
            l.append(ipv4.src)
            l.append(ipv4.target)
          #  print(TAB_1 + 'IPv4 Packet:')
           # print(TAB_2 + 'Version: {}, Header Length: {}, TTL: {},'.format(ipv4.version, ipv4.header_length, ipv4.ttl))
            Data+=TAB_1 + 'IPv4 Packet:'+TAB_2 + 'Version:'+str(ipv4.version)+'Header Length:'+ str(ipv4.header_length)+'TTL:'+str(ipv4.ttl)
            l.append(ipv4.header_length)

            # ICMP
            if ipv4.proto == 1:
                icmp = ICMP(ipv4.data)
                l.append('ICMP')
            #    print(TAB_1 + 'ICMP Packet:')
             #   print(TAB_2 + 'Type: {}, Code: {}, Checksum: {},'.format(icmp.type, icmp.code, icmp.checksum))
              #  print(TAB_2 + 'ICMP Data:')
               # print(format_multi_line(DATA_TAB_3, icmp.data))
                Data+=TAB_1 + 'ICMP Packet:'+TAB_2 + 'Type: '+str(icmp.type)+"Code:"+str(icmp.code)+"Checksum:"+str( icmp.checksum)+TAB_2 + 'ICMP Data:'+str(format_multi_line(DATA_TAB_3, icmp.data))
                l.append(icmp.data)
                l.append(" ")

            # TCP
            elif ipv4.proto == 6:
                tcp = TCP(ipv4.data)
                #print(TAB_1 + 'TCP Segment:')
                l.append('TCP')
                #print(TAB_2 + 'Source Port: {}, Destination Port: {}'.format(tcp.src_port, tcp.dest_port))
                info+=str(tcp.src_port)+"->"+str(tcp.dest_port)+"ACK="+str(tcp.flag_ack)+"len ="+str(len(tcp.data))
                #print(TAB_2 + 'Sequence: {}, Acknowledgment: {}'.format(tcp.sequence, tcp.acknowledgment))
                #print(TAB_2 + 'Flags:')
                #print(TAB_3 + 'URG: {}, ACK: {}, PSH: {}'.format(tcp.flag_urg, tcp.flag_ack, tcp.flag_psh))
                #print(TAB_3 + 'RST: {}, SYN: {}, FIN:{}'.format(tcp.flag_rst, tcp.flag_syn, tcp.flag_fin))
                Data+=TAB_1 + 'TCP Segment:'+TAB_2 + 'Source Port:'+str(tcp.src_port)+"Destination Port:"+str( tcp.dest_port)+TAB_2 + 'Sequence:'+str(tcp.sequence)+" Acknowledgment:"+str(tcp.acknowledgment)
                Data+=TAB_2 + 'Flags:'+TAB_3 + 'URG:'+str(tcp.flag_urg)+'ACK'+str(tcp.flag_ack)+'PSH'+str(tcp.flag_psh)+TAB_3 + 'RST:'+str(tcp.flag_rst)+'SYN'+str(tcp.flag_syn)+'FIN'+str(tcp.flag_fin)
                l.append(tcp.data)
                l.append(info)
                if len(tcp.data) > 0:

                    # HTTP
                    if tcp.src_port == 80 or tcp.dest_port == 80:
                        Data+=TAB_2 + 'HTTP Data:'
                 #       print(TAB_2 + 'HTTP Data:')
                        try:
                            http = HTTP(tcp.data)
                            http_info = str(http.data).split('\n')
                            for line in http_info:
                                Data+=DATA_TAB_3 + str(line)
                  #              print(DATA_TAB_3 + str(line))
                        except:
                   #         print(format_multi_line(DATA_TAB_3, tcp.data))
                            Data+=format_multi_line(DATA_TAB_3, tcp.data)
                    else:
                    #    print(TAB_2 + 'TCP Data:')
                     #   print(format_multi_line(DATA_TAB_3, tcp.data))
                        Data+=TAB_2 + 'TCP Data:'+format_multi_line(DATA_TAB_3, tcp.data)

            # UDP
            elif ipv4.proto == 17:
                udp = UDP(ipv4.data)
                l.append('UDB')
                #print(TAB_1 + 'UDP Segment:')
                #print(TAB_2 + 'Source Port: {}, Destination Port: {}, Length: {}'.format(udp.src_port, udp.dest_port, udp.size))
                Data+=TAB_1 + 'UDP Segment:'+TAB_2 + 'Source Port:'+str(udp.src_port)+'Destination Port:'+str( udp.dest_port)+'Length'+str(udp.size)
                info += str(udp.src_port) + "->" +str (udp.dest_port) + "len =" + str(udp.size) # + "ACK=" + str(udp.flag_ack)
                l.append(0)
                l.append(info)

            # Other IPv4
            else:
                #print(TAB_1 + 'Other IPv4 Data:')
                l.append('other')
                l.append(0)
                l.append('other')
                #print(format_multi_line(DATA_TAB_2, ipv4.data))
                Data+=TAB_1 + 'Other IPv4 Data:'+format_multi_line(DATA_TAB_2, ipv4.data)

        else:
            #print('Ethernet Data:')
            #print(format_multi_line(DATA_TAB_1, eth.data))
            l.append(" ")#src
            l.append(" ")#target
            l.append(" ")#Hlength
            l.append(" ")#protocol
            Data+='Ethernet Data:'+format_multi_line(DATA_TAB_1, eth.data)
            l.append(format_multi_line(DATA_TAB_1, eth.data))#hex
            l.append(" ")  # info
        l.append(Data)
        temp=l[3]
        l[3]=l[4]
        l[4]=temp
        temp2=l[5]
        l[5]=l[6]
        l[6]=l[7]
        l[7]=temp2
        print (*l ,sep=',')
        info=""
        Data=""


    pcap.close()



main()
