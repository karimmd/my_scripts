/*
TCPTestRouteMod v0.1
Two nodes communicating over PPP with TCP protocol
There is a rouing node in the middle.
*/

#include "ns3/netanim-module.h"
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"

using namespace ns3;
Ptr<OutputStreamWrapper> cWndStream;

NS_LOG_COMPONENT_DEFINE ("TCPTest");

class TestApp : public Application{
public:
  TestApp() : m_socket (0),
    m_peer (),
    m_packetSize (0),
    m_nPackets (0),
    m_dataRate (0),
    m_sendEvent (),
    m_running (false),
    m_packetsSent (0) {
  }
  ~TestApp() {
    m_socket = 0;
  }

  void Setup(Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate datarate) {
    m_socket = socket;
    m_peer = address;
    m_packetSize = packetSize;
    m_nPackets = nPackets;
    m_dataRate = datarate;
  }

private:
  //Over riding fucntions. MUST be overriding.
  virtual void StartApplication(void);
  virtual void StopApplication(void);


  // Send packet and schdule next unless max packets achieved.
  void SendPacket() {
    Ptr<Packet> packet = Create<Packet> (m_packetSize);
    m_socket->Send(packet);
    if (++m_packetsSent < m_nPackets) {
      if(m_running) {
        Time tNext (Seconds(m_packetSize*8/static_cast<double> (m_dataRate.GetBitRate())) );
        m_sendEvent = Simulator::Schedule(tNext, &TestApp::SendPacket, this);
      }
    }
  }

  // Variables
  Ptr<Socket>     m_socket;
  Address         m_peer;
  uint32_t        m_packetSize;
  uint32_t        m_nPackets;
  DataRate        m_dataRate;
  EventId         m_sendEvent;
  bool            m_running;
  uint32_t        m_packetsSent;
};

void
TestApp::StartApplication(void) {
  m_running = true;
  m_packetsSent = 0;
  m_socket->Bind();
  m_socket->Connect(m_peer);
  SendPacket();
}

void
TestApp::StopApplication(void) {
  m_running = false;
  if (m_sendEvent.IsRunning()) {
    Simulator::Cancel(m_sendEvent);
  }

  if (m_socket) {
    m_socket->Close();
  }
}

static void
cWndTracer (uint32_t oldCwnd, uint32_t newCwnd)
{
  //*cWndStream->GetStream() << Now ().GetSeconds () << "\t" << newCwnd << "\n";
  NS_LOG_UNCOND (Simulator::Now ().GetSeconds () << "\t" << newCwnd);
}

static void
ssThreshTracer (uint32_t oldval, uint32_t newval)
{
  //NS_LOG_UNCOND (Simulator::Now ().GetSeconds () << "\t\t" << newval);
}

static void
RxDrop (Ptr<const Packet> p)
{
  //NS_LOG_UNCOND ("RxDrop at " << Simulator::Now ().GetSeconds ());
}


int main ()
{
    Time::SetResolution(Time::NS);
    LogComponentEnable("TCPTest", LOG_LEVEL_INFO);

    //Creating 3 nodes. 2 will be source dest pair, the thrid will be in the middle.
    NS_LOG_INFO("Creating Nodes");
    NodeContainer nodes;
    nodes.Create(3);

    // Specifying flavor of TCP. Has to be done before creation of stack
    //Config::SetDefault("ns3::TcpL4Protocol::SocketType", TypeIdValue(TcpNewReno::GetTypeId()));

    NS_LOG_INFO("Creating PPP link");
    PointToPointHelper p2p;
    p2p.SetDeviceAttribute("DataRate", StringValue ("5Mbps"));
    p2p.SetChannelAttribute("Delay", StringValue("2ms"));

    NS_LOG_INFO("Creating NetDevices and linking via p2p");
    NetDeviceContainer devicesd0d1 = p2p.Install(nodes.Get(0), nodes.Get(1));
    NetDeviceContainer devicesd1d2 = p2p.Install(nodes.Get(1), nodes.Get(2));

    //Error Model on receiging node (N2)
    Ptr<RateErrorModel> em = CreateObject<RateErrorModel> ();
    em->SetAttribute ("ErrorRate", DoubleValue (0.00002));
    devicesd1d2.Get(1)->SetAttribute ("ReceiveErrorModel", PointerValue (em));

    NS_LOG_INFO("Installing stack");
    InternetStackHelper stack;
    stack.Install(nodes);

    NS_LOG_INFO("Assigning IP Addresses to devicesd0d1");
    Ipv4AddressHelper address;
    address.SetBase("10.1.1.0", "255.255.255.0");
    Ipv4InterfaceContainer interfacesi0i1 = address.Assign(devicesd0d1);
    NS_LOG_INFO("Assigning IP Addresses to devicesd1d2");
    address.SetBase("10.1.2.0", "255.255.255.0");
    Ipv4InterfaceContainer interfacesi1i2 = address.Assign(devicesd1d2);

    NS_LOG_INFO("Creating Routing Tables");
    Ipv4GlobalRoutingHelper::PopulateRoutingTables();

    NS_LOG_INFO("Creating Sink Application");
    uint16_t sinkPort = 8080;
    Address sinkAddress(InetSocketAddress(interfacesi1i2.GetAddress(1), sinkPort));
    PacketSinkHelper packetSinkHelper("ns3::TcpSocketFactory", sinkAddress);

    ApplicationContainer sinkApp = packetSinkHelper.Install(nodes.Get(2));
    sinkApp.Start(Seconds(0.0));
    sinkApp.Stop(Seconds(20.0));

    NS_LOG_INFO("Creating Source App");
    //Create scoket first, and then install the app on node using that socket
    Ptr<Socket> sourceTcpSocket = Socket::CreateSocket(nodes.Get(0), TcpSocketFactory::GetTypeId());

    //connecting trace source with sink function (can be done later too)
    sourceTcpSocket->TraceConnectWithoutContext ("CongestionWindow", MakeCallback (&cWndTracer));
    sourceTcpSocket->TraceConnectWithoutContext ("SlowStartThreshold", MakeCallback (&ssThreshTracer));

    //Creating object of app and set up on node
    Ptr<TestApp> sourceApp = CreateObject<TestApp> ();
    sourceApp->Setup(sourceTcpSocket, sinkAddress, 1040, 1000, DataRate("1Mbps"));
    nodes.Get(0)->AddApplication(sourceApp);
    sourceApp->SetStartTime(Seconds(1.0));
    sourceApp->SetStopTime(Seconds(20.0));

    devicesd1d2.Get(1)->TraceConnectWithoutContext ("PhyRxDrop", MakeCallback (&RxDrop));

    //Enabling Pcap Tracing
    p2p.EnablePcapAll("scratch/TCPTestRouteMod");

    //Initializing the cWndStream
    AsciiTraceHelper asciiTraceHelper;
    cWndStream = asciiTraceHelper.CreateFileStream("cWndValues.dat");

    Simulator::Stop(Seconds(20.0));
    NS_LOG_INFO("Starting Simulator");
    Simulator::Run ();
    NS_LOG_INFO("Destroying Simulator");
    Simulator::Destroy ();

    return 0;
}