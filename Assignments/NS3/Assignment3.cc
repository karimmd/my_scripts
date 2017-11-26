#include <fstream>
#include <string>
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/internet-module.h"
#include "ns3/flow-monitor-module.h"
#include "ns3/ipv4-global-routing-helper.h"
#include "ns3/netanim-module.h"
#include "ns3/tcp-header.h"
#include "ns3/udp-header.h"
#include "ns3/traffic-control-module.h"


using namespace ns3;


NS_LOG_COMPONENT_DEFINE ("Assignment");

class MyApp : public Application
{
public:

  MyApp ();
  virtual ~MyApp();

  void Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate);
  void ChangeRate(DataRate newrate);

private:
  virtual void StartApplication (void);
  virtual void StopApplication (void);

  void ScheduleTx (void);
  void SendPacket (void);

  Ptr<Socket>     m_socket;
  Address         m_peer;
  uint32_t        m_packetSize;
  uint32_t        m_nPackets;
  DataRate        m_dataRate;
  EventId         m_sendEvent;
  bool            m_running;
  uint32_t        m_packetsSent;
};

MyApp::MyApp ()
  : m_socket (0),
    m_peer (),
    m_packetSize (0),
    m_nPackets (0),
    m_dataRate (0),
    m_sendEvent (),
    m_running (false),
    m_packetsSent (0)
{
}

MyApp::~MyApp()
{
  m_socket = 0;
}

void
MyApp::Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate)
{
  m_socket = socket;
  m_peer = address;
  m_packetSize = packetSize;
  m_nPackets = nPackets;
  m_dataRate = dataRate;
}

void
MyApp::StartApplication (void)
{
  m_running = true;
  m_packetsSent = 0;
  m_socket->Bind ();
  m_socket->Connect (m_peer);
  SendPacket ();
}

void
MyApp::StopApplication (void)
{
  m_running = false;

  if (m_sendEvent.IsRunning ())
    {
      Simulator::Cancel (m_sendEvent);
    }

  if (m_socket)
    {
      m_socket->Close ();
    }
}

void
MyApp::SendPacket (void)
{
  Ptr<Packet> packet = Create<Packet> (m_packetSize);
  m_socket->Send (packet);

  if (++m_packetsSent < m_nPackets)
    {
      ScheduleTx ();
    }
}

void
MyApp::ScheduleTx (void)
{
  if (m_running)
    {
      Time tNext (Seconds (m_packetSize * 8 / static_cast<double> (m_dataRate.GetBitRate ())));
      m_sendEvent = Simulator::Schedule (tNext, &MyApp::SendPacket, this);
    }
}

void
MyApp::ChangeRate(DataRate newrate)
{
   m_dataRate = newrate;
   return;
}

static void
CwndChange (uint32_t oldCwnd, uint32_t newCwnd)
{
  std::cout << Simulator::Now ().GetSeconds () << "\t" << newCwnd <<"\n";
}

void
IncRate (Ptr<MyApp> app, DataRate rate)
{
	app->ChangeRate(rate);
    return;
}


int main ()
{

  std::string lat = "2ms";
  std::string rate = "5Mbps";		 // P2P link
  std::string rate1="2Mbps"; 		// for Node 3 to 4
  bool enableFlowMonitor = false;



  CommandLine cmd;
  cmd.AddValue ("latency", "P2P link Latency in seconds", lat);
  cmd.AddValue ("rate", "P2P data rate in bps", rate);
  cmd.AddValue ("EnableMonitor", "Enable Flow Monitor", enableFlowMonitor);

  //cmd.Parse (argc, argv);


  // Specifying flavor of TCP. Has to be done before creation of stack
  Config::SetDefault("ns3::TcpL4Protocol::SocketType", TypeIdValue(TcpYeah::GetTypeId()));


//***************** Nodes Creation required by the topology as Shown above********************

  NS_LOG_INFO ("Create nodes.");
  NodeContainer c; // ALL Nodes
  c.Create(8);

  NodeContainer n0n3 = NodeContainer (c.Get (0), c.Get (3));
  NodeContainer n1n3 = NodeContainer (c.Get (1), c.Get (3));
  NodeContainer n2n3 = NodeContainer (c.Get (2), c.Get (3));
  NodeContainer n3n4 = NodeContainer (c.Get (3), c.Get (4));
  NodeContainer n5n4 = NodeContainer (c.Get (5), c.Get (4));
  NodeContainer n6n4 = NodeContainer (c.Get (6), c.Get (4));
  NodeContainer n7n4 = NodeContainer (c.Get (7), c.Get (4));



//************************ Install Internet Stack*********************************

  InternetStackHelper internet;
  internet.Install (c);

//**************** channels Creation without IP addressing*************************

  NS_LOG_INFO ("Create channels.");
  PointToPointHelper p2p,p2p_for3_4;
  p2p.SetDeviceAttribute ("DataRate", StringValue (rate));
  p2p.SetChannelAttribute ("Delay", StringValue (lat));
  NetDeviceContainer d0d3 = p2p.Install (n0n3);
  NetDeviceContainer d1d3 = p2p.Install (n1n3);
  NetDeviceContainer d2d3 = p2p.Install (n2n3);
  NetDeviceContainer d5d4 = p2p.Install (n5n4);
  NetDeviceContainer d6d4 = p2p.Install (n6n4);
  NetDeviceContainer d7d4 = p2p.Install (n7n4);

  p2p_for3_4.SetDeviceAttribute ("DataRate", StringValue (rate1)); // for Node 3 to 4 data rate is 2Mbps
  p2p_for3_4.SetChannelAttribute ("Delay", StringValue (lat));
  NetDeviceContainer d3d4 = p2p_for3_4.Install (n3n4);


//*********************IP addresses Setup******************************************

  NS_LOG_INFO ("Assign IP Addresses.");
  Ipv4AddressHelper ipv4;
  ipv4.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer i0i3 = ipv4.Assign (d0d3);

  ipv4.SetBase ("10.1.2.0", "255.255.255.0");
  Ipv4InterfaceContainer i1i3 = ipv4.Assign (d1d3);

  ipv4.SetBase ("10.1.3.0", "255.255.255.0");
  Ipv4InterfaceContainer i2i3 = ipv4.Assign (d2d3);

  ipv4.SetBase ("10.1.4.0", "255.255.255.0");
  Ipv4InterfaceContainer i3i4 = ipv4.Assign (d3d4);

  ipv4.SetBase ("10.1.5.0", "255.255.255.0");
  Ipv4InterfaceContainer i5i4 = ipv4.Assign (d5d4);

  ipv4.SetBase ("10.1.6.0", "255.255.255.0");
  Ipv4InterfaceContainer i6i4 = ipv4.Assign (d6d4);

  ipv4.SetBase ("10.1.7.0", "255.255.255.0");
  Ipv4InterfaceContainer i7i4 = ipv4.Assign (d7d4);


   NS_LOG_INFO ("Enable static global routing.");


  //***************** Turn on global static routing for routing across the network******************
  Ipv4GlobalRoutingHelper::PopulateRoutingTables ();


  NS_LOG_INFO ("Create Applications.");



  //************** TCP connection from N1 to N6**********************************************
  uint16_t sinkPort = 8080;
  Address sinkAddress (InetSocketAddress (i6i4.GetAddress (0), sinkPort));         // Interface of N6
  PacketSinkHelper packetSinkHelper ("ns3::TcpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), sinkPort));
  ApplicationContainer sinkApps = packetSinkHelper.Install (c.Get (6));                //N6 as sink
  sinkApps.Start (Seconds (5.));
//  sinkApps.Stop (Seconds (25.));


  Ptr<Socket> ns3TcpSocket1 = Socket::CreateSocket (c.Get (1), TcpSocketFactory::GetTypeId ()); //source at N1

  //********************* Congestion window**********************
  ns3TcpSocket1->TraceConnectWithoutContext ("CongestionWindow", MakeCallback (&CwndChange));

  //*********************TCP application at N1*******************************
  Ptr<MyApp> app = CreateObject<MyApp> ();
  app->Setup (ns3TcpSocket1, sinkAddress, 1040, 100000, DataRate ("1Mbps"));
  c.Get (1)->AddApplication (app);
  app->SetStartTime (Seconds (5.));
//  app->SetStopTime (Seconds (25.));

  // *********************UDP connection from N2 to N7 ****************************

  uint16_t sinkPort2 = 6;
  Address sinkAddress2 (InetSocketAddress (i7i4.GetAddress (0), sinkPort2)); // interface of n7
  PacketSinkHelper packetSinkHelper2 ("ns3::UdpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), sinkPort2));
  ApplicationContainer sinkApps2 = packetSinkHelper2.Install (c.Get (7)); //n7 as sink
  sinkApps2.Start (Seconds (10.));
  sinkApps2.Stop (Seconds (17.));

  Ptr<Socket> ns3UdpSocket = Socket::CreateSocket (c.Get (2), UdpSocketFactory::GetTypeId ()); //source at n2

  // Create UDP application at N2
  Ptr<MyApp> app2 = CreateObject<MyApp> ();
  app2->Setup (ns3UdpSocket, sinkAddress2, 1040, 100000, DataRate ("1Mbps"));
  c.Get (2)->AddApplication (app2);
  app2->SetStartTime (Seconds (10.));
  app2->SetStopTime (Seconds (17.));

// Increase UDP Rate
//  Simulator::Schedule (Seconds(20.0), &IncRate, app2, DataRate("2Mbps"));

  // Flow Monitor
  Ptr<FlowMonitor> flowmon;
  if (enableFlowMonitor)
    {
      FlowMonitorHelper flowmonHelper;
      flowmon = flowmonHelper.InstallAll ();
    }



//
// Now, do the actual simulation.
//

  NS_LOG_INFO ("Run Simulation.");
  Simulator::Stop (Seconds(25.0));

   //Enabling Pcap Tracing
   //p2p.EnablePcapAll("scratch/Assignment3");


  AnimationInterface anim("Assignment3.xml");
  anim.SetConstantPosition(c.Get(0),0.0,0.0);
  anim.SetConstantPosition(c.Get(1),0.0,2.0);
  anim.SetConstantPosition(c.Get(2),0.0,4.0);
  anim.SetConstantPosition(c.Get(3),2.0,2.0);
  anim.SetConstantPosition(c.Get(4),4.0,2.0);
  anim.SetConstantPosition(c.Get(5),6.0,0.0);
  anim.SetConstantPosition(c.Get(6),6.0,2.0);
  anim.SetConstantPosition(c.Get(7),6.0,4.0);

  Simulator::Run ();
  if (enableFlowMonitor)
    {
	  flowmon->CheckForLostPackets ();
	  flowmon->SerializeToXmlFile("Assignment3.flowmon", true, true);
    }
  Simulator::Destroy ();
  NS_LOG_INFO ("Done.");
}
