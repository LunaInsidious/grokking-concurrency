## アドレスファミリ

AF_INET(IPv4),AF_INET6(IPv6),AF_UNIX(local to host (pipes, portals))くらいしか使わないらしい

<details>
<summary>pythonのAddressFamilyの定義</summary>

```python
class AddressFamily(IntEnum):
    AF_INET = 2
    AF_INET6 = 10
    AF_APPLETALK = 5
    AF_DECnet = ...
    AF_IPX = 4
    AF_SNA = 22
    AF_UNSPEC = 0
    if sys.platform != "darwin":
        AF_IRDA = 23
    if sys.platform != "win32":
        AF_ROUTE = 16
        AF_SYSTEM = 32
        AF_UNIX = 1
    if sys.platform != "win32" and sys.platform != "darwin":
        AF_AAL5 = ...
        AF_ASH = 18
        AF_ATMPVC = 8
        AF_ATMSVC = 20
        AF_AX25 = 3
        AF_BRIDGE = 7
        AF_ECONET = 19
        AF_KEY = 15
        AF_LLC = 26
        AF_NETBEUI = 13
        AF_NETROM = 6
        AF_PPPOX = 24
        AF_ROSE = 11
        AF_SECURITY = 14
        AF_WANPIPE = 25
        AF_X25 = 9
    if sys.platform == "linux":
        AF_CAN = 29
        AF_PACKET = 17
        AF_RDS = 21
        AF_TIPC = 30
        AF_ALG = 38
        AF_NETLINK = 16
        AF_VSOCK = 40
        AF_QIPCRTR = 42
    if sys.platform != "win32" or sys.version_info >= (3, 9):
        AF_LINK = 33
        if sys.platform != "darwin":
            AF_BLUETOOTH = 32
    if sys.platform == "win32" and sys.version_info >= (3, 12):
        AF_HYPERV = 34
    if sys.platform != "linux" and sys.platform != "win32" and sys.platform != "darwin" and sys.version_info >= (3, 12):
        # FreeBSD >= 14.0
        AF_DIVERT = 44
```
</details>

<details>
<summary>それぞれのAddressFamilyのChatGPT o1の解説</summary>
以下では、コード内で列挙されているアドレスファミリ (AddressFamily) それぞれについて、主にどのような用途・歴史的背景を持つかなどを簡単に解説します。なお、実際の数値やサポート状況はプラットフォームによって異なる場合があります。また、Python でのマッピングも OS やバージョンによって違いが生じることに注意してください。

### 汎用的/主要なアドレスファミリ
1. AF_UNSPEC (0)
「未指定」を表すアドレスファミリです。ソケット生成時などに特定のアドレスファミリを指定しない場合や、汎用的に使われる際に用いられます。

1. AF_UNIX (1)
UNIX ドメインソケット(ローカルソケット)用のアドレスファミリです。ファイルシステム上のパスを使って同一マシン内でのプロセス間通信(IPC)に用いられます。

1. AF_INET (2)
IPv4 用のアドレスファミリです。最も一般的なインターネット通信プロトコル (TCP/UDP over IPv4) で使われます。

1. AF_INET6 (10)
IPv6 用のアドレスファミリです。IPv4 のアドレス枯渇問題への対策として策定された IPv6 の通信 (TCP/UDP over IPv6) で使われます。

### その他のアドレスファミリ (歴史的なものや特殊用途のもの)

1. AF_APPLETALK (5)
Apple がかつて用いていた AppleTalk プロトコル用のアドレスファミリ。古い Mac OS 同士のネットワーク通信などに使われていましたが、現在ではほぼ使われません。

1. AF_DECnet (…省略値…)
DEC(Digital Equipment Corporation) が開発した DECnet 用のアドレスファミリ。VAX 系システムを中心に使われていましたが、現在ではレガシーとなっています。

1. AF_IPX (4)
Novell NetWare で用いられた IPX(Internetwork Packet Exchange) プロトコル用のアドレスファミリ。かつての LAN やゲーム(例: Doom, Quake) マルチプレイで使われた歴史があります。

1. AF_SNA (22)
IBM のメインフレーム用通信プロトコル SNA(Systems Network Architecture) のアドレスファミリ。メインフレーム環境向けのレガシープロトコルです。

1. AF_IRDA (23)
赤外線通信 IrDA(Infrared Data Association) 用のアドレスファミリ。かつてノート PC や携帯端末などの赤外線ポート間通信で使われました。

1. AF_ROUTE (16)
BSD 系 OS でルーティング情報を扱うためのアドレスファミリ。ルーティングソケットとも呼ばれ、カーネルのルーティングテーブルの操作などに利用されます。

1. AF_SYSTEM (32)
macOS/iOS (Darwin) で内部的なシステム連携を行うためのアドレスファミリ。カーネル拡張などの一部機能で使われます。

1. AF_AAL5 (…省略値…)
ATM (Asynchronous Transfer Mode) で利用される AAL5(ATM Adaptation Layer 5) 用のアドレスファミリ。ATM ベースのネットワークでパケットをカプセル化/復号するときに使われます。

1. AF_ASH (18)
いくつかのアマチュア無線向けプロトコルや、ドイツのアマチュア無線ネットワーク (ASH) に関係するアドレスファミリとされますが、非常に特殊です。

1. AF_ATMPVC (8)
ATM PVC (Permanent Virtual Circuit) 用のアドレスファミリ。ATM 回線における恒久的な仮想回線での通信を扱います。

1. AF_ATMSVC (20)
ATM SVC (Switched Virtual Circuit) 用のアドレスファミリ。スイッチ経由でオンデマンドに回線を確立する ATM 通信を扱います。

1. AF_AX25 (3)
アマチュア無線で使われる AX.25 プロトコル用のアドレスファミリ。アマチュアパケット無線の一形態です。

1. AF_BRIDGE (7)
Ethernet ブリッジなど、低レベルでのブリッジ処理を行う際のアドレスファミリです。カーネルブリッジ機能などとやり取りをするときに使います。

1. AF_ECONET (19)
かつて Acorn コンピュータなどで使われた Econet プロトコル用のアドレスファミリ。イギリス発祥の古いネットワーク技術です。

1. AF_KEY (15)
IPsec などのキー管理 (Key Management) を行うためのアドレスファミリ。暗号鍵やセキュリティ関連の設定をやり取りするために用いられます。

1. AF_LLC (26)
LLC (Logical Link Control) 層に関連したアドレスファミリ。OSI 参照モデルのデータリンク層にあたるものを扱います。

1. AF_NETBEUI (13)
NetBIOS Extended User Interface (NetBEUI) プロトコル用のアドレスファミリ。Microsoft LAN Manager や IBM LAN Server などの古い LAN 通信に使われました。

1. AF_NETROM (6)
アマチュア無線通信の中でも NetRom プロトコルを扱うアドレスファミリ。AX.25 上で動作するルーティングプロトコルの一種です。

1. AF_PPPOX (24)
PPPoX (PPP over “X”) をサポートするアドレスファミリ。PPP over Ethernet (PPPoE) などのバリエーションを扱うために使われます。

1. AF_ROSE (11)
アマチュア無線用の X.25ネットワーク (ROSE: ROuting and SEssion) で使われるアドレスファミリ。こちらも主にアマチュア無線で利用されます。

1. AF_SECURITY (14)
セキュリティモジュール (LSM: Linux Security Modules) などでのフックやコールバックに用いられるアドレスファミリ。Linux カーネルのセキュリティ関連で登場します。

1. AF_WANPIPE (25)
Sangoma WANPIPE カードなど、専用の WAN インターフェイスを扱うためのアドレスファミリ。

1. AF_X25 (9)
X.25 プロトコル用のアドレスファミリ。古いパケット交換ネットワーク (公衆電話網ベース) で利用されました。

### Linux 特有のアドレスファミリ

1. AF_CAN (29)
CAN (Controller Area Network) 用のアドレスファミリ。自動車などの制御装置間通信に広く利用されているプロトコルです。

1. AF_PACKET (17)
リンク層パケットインターフェイス用のアドレスファミリ。RAW ソケットを使って直接 Ethernet フレームを送受信する際などに用いられます。

1. AF_RDS (21)
RDS(Reliable Datagram Sockets) 用のアドレスファミリ。高い信頼性と低遅延を提供するよう設計されたプロトコルで、クラスタ間通信などで使われます。

1. AF_TIPC (30)
TIPC(Transparent Inter-Process Communication) 用のアドレスファミリ。クラスタリングされた分散環境での高速 IPC を目的としています。

1. AF_ALG (38)
Linux カーネルの暗号 API (crypto API) に対してユーザースペースからアクセスするための “Kernel Algorithm” ソケット。暗号処理をユーザ空間から利用するために使われます。

1. AF_NETLINK (16)
Linux カーネルとユーザ空間間の通信を行う Netlink ソケット用のアドレスファミリ。ルーティング情報のやり取りやファイアウォール設定など、さまざまなサブシステムが活用します。

1. AF_VSOCK (40)
仮想マシン (VM) とホスト間での高速通信を行うための “VM Sockets” 用アドレスファミリ (例: VMware, virtio-vsock など)。Hypervisor 内部での IPC に使われます。

1. AF_QIPCRTR (42)
Qualcomm MSM デバイス上の IPC Routing (QRTR) に使われるアドレスファミリ。主に Android デバイスなど Qualcomm プラットフォームにおける IPC を扱います。

### BSD / macOS / その他のアドレスファミリ

1. AF_LINK (33)
BSD 系 OS や macOS でリンク層 (Ethernet MAC アドレスなど) を直接扱うために使われるアドレスファミリです。
Linux では同様の用途として AF_PACKET が使われることが多いです。

1. AF_BLUETOOTH (32)
Bluetooth 通信用のアドレスファミリ。macOS などでは AF_SYSTEM=32 と衝突する場合もあり、実装依存で異なる値になることもあります。

### Windows 特有 / バージョン依存のアドレスファミリ
1. AF_HYPERV (34)
Windows Hyper-V 上での仮想マシンとの通信に使われるアドレスファミリ。
sys.platform == "win32" かつ Python 3.12 以降でサポートされます。

### FreeBSD 新バージョン特有

1. AF_DIVERT (44)
FreeBSD 14.0 以降 (かつ Linux / Windows / macOS 以外) でサポートされる “divert sockets” 用のアドレスファミリ。ファイアウォール(pf, ipfw)などでパケットをユーザ空間に振り分ける機能で使われます。

### まとめ
- AF_INET / AF_INET6 / AF_UNIX は最もよく使われる主要なアドレスファミリ。
- AF_PACKET / AF_NETLINK / AF_CAN などは主に Linux 向けの低レベル機能。
- AF_ROUTE / AF_LINK は BSD 系 OS 向けの機能。
- AF_SYSTEM / AF_BLUETOOTH などは macOS / iOS で固有な設定を扱う場合に登場。
- AF_HYPERV は最新の Windows Hyper-V サポート。
- ATM 系 (AF_ATMPVC / AF_ATMSVC / AF_AAL5) や X.25 系 は現在ではほぼレガシー。
- アマチュア無線系 (AX.25, NetRom, ROSE, ASH) は特殊用途。
- AF_DIVERT は FreeBSD でのファイアウォール制御用。

このように、アドレスファミリは OS 内部のネットワークスタックや、特定の通信プロトコルと密接に結びついており、実際に利用される・サポートされるかどうかはプラットフォームやバージョンによって異なります。
</details>

### 参考文献

[アドレスファミリを簡単にまとめたサイト](https://www.geekpage.jp/programming/winsock/addressfamily.php#google_vignette)
[osの種類について](https://qiita.com/zawawahoge/items/2ec3b638422c7c8cac8f)

## ソケットタイプ

<details>
<summary>pythonのSocketKindの定義</summary>

```python
class SocketKind(IntEnum):
    SOCK_STREAM = 1
    SOCK_DGRAM = 2
    SOCK_RAW = 3
    SOCK_RDM = 4
    SOCK_SEQPACKET = 5
    if sys.platform == "linux":
        SOCK_CLOEXEC = 524288
        SOCK_NONBLOCK = 2048
```
</details>

<details>
<summary>それぞれのSocketKindのChatGPT o1の解説</summary>

以下では、SocketKind の各値が何を表しているのか、簡単に解説します。

1. SOCK_STREAM (1)
TCP などのコネクション型通信に利用するソケットタイプです。ストリーム通信を行うため、接続の確立（コネクション）が必要となり、到着順序の保証や再送などの機能が備わっています。

1. SOCK_DGRAM (2)
UDP などのデータグラム型通信に利用するソケットタイプです。コネクション不要（コネクションレス）で、届く順番やデータ欠損の保証はありませんが、オーバーヘッドが少なく、リアルタイム性を求められる用途などで使われます。

1. SOCK_RAW (3)
IP ヘッダなどを直接操作したり、プロトコルレベルで細かい制御を行うための生ソケットです。パケットの送受信をより低レベルな形式で行うため、ネットワークのテストやパケット解析などで利用されます。

1. SOCK_RDM (4)
“Reliable Datagram” の略とされるソケットタイプですが、対応していないプラットフォームも多く、実際にはあまり使われていません。データグラム型でありながら信頼性をある程度担保する仕組みを備えたもの、という位置づけです。

1. SOCK_SEQPACKET (5)
シーケンシャル・パケット型ソケットで、データグラムのようにメッセージ単位で送受信しつつ、到着順序やコネクションなどを管理します。UNIX ドメインソケット（AF_UNIX）の SOCK_SEQPACKET などで利用されることがあります。

1. SOCK_CLOEXEC (524288, Linux のみ)
「close-on-exec」フラグを表します。ソケットを作成するときにこのフラグを指定すると、exec 系のシステムコールを実行した際に、そのソケットが自動的にクローズされます。セキュリティやファイルディスクリプタ管理のために使われます。

1. SOCK_NONBLOCK (2048, Linux のみ)
ソケットをノンブロッキングモードで動作させるためのフラグです。ソケット操作（send/recv など）がブロック（待ち状態）にならず、すぐに処理を継続するようになります。GUI アプリケーションやサーバの高負荷処理など、待ちを極力減らしたい状況で使われます。
</details>
