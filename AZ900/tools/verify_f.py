# -*- coding: utf-8 -*-
"""核對原文 批次 F：#426 #427 #461 #464 #469 #472（PDF 第 125、134、135、137、138 頁）。
   同時把解析改寫成「共用對照一次 + 逐格重點」，並統一 Advisor 的中譯。
   一次性腳本，保留供追溯。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vfy import load, save, patch, js, arr, arr2

L = load()

# ══ #426（PDF 第 125 頁）═════════════════════════════════════════════
E426 = """三個雲端效益一次分清楚：
・⟦彈性（Elasticity）⟧— 依實際負載自動增減資源，用多少付多少。談的是「量能隨需求上下」，而且是自動、動態的。與可擴縮性（Scalability）常被混用，細分的話：可擴縮性強調「能不能長大」，彈性強調「能自動長大也能自動縮回」。
・⟦敏捷性（Agility）⟧— 從想到到做出來的速度。雲端上開一台虛擬機器、一個資料庫只要幾分鐘，不必採購、不必等機器進機房、不必估三年的容量。談的是「快」，不是「量」。
・⟦災難復原（Disaster recovery）⟧— 中斷或災害之後把服務與資料復原起來，靠異地備份與 Azure Site Recovery，兩個關鍵指標是 RTO（多久之內恢復）與 RPO（最多能掉多少資料）。
一句話分：⟦彈性＝資源量自動跟著需求走；敏捷性＝東西做得快；災難復原＝壞了救得回來⟧。

【能夠動態調整某個雲端應用程式可用的資源】→ 彈性（Elasticity）
關鍵字是「動態調整資源」。有「自動、隨需求」的味道就是彈性。

【能夠在發生中斷事件時，使用雲端的備份服務還原資源】→ 災難復原（Disaster recovery）
關鍵字是「中斷」加「還原」。壞掉之後救回來就是災難復原。

【能夠在應用程式需求改變時，快速部署與設定雲端資源】→ 敏捷性（Agility）
關鍵字是「快速部署與設定」。這裡講的是速度，不是資源多寡，所以不是彈性。"""

EN426 = """Separate the three cloud benefits once:
・⟦Elasticity⟧ — resources grow and shrink automatically with actual load, and you pay for what you use. It is about capacity following demand, automatically and dynamically. It overlaps with scalability; the fine distinction is that scalability is about being able to grow, while elasticity is about growing and shrinking on its own.
・⟦Agility⟧ — how fast an idea becomes a running thing. A VM or a database in the cloud takes minutes: no purchase order, no waiting for hardware to arrive, no three-year capacity guess. It is about speed, not amount.
・⟦Disaster recovery⟧ — restoring services and data after an outage or disaster, using off-site backup and Azure Site Recovery, measured by RTO (how soon service returns) and RPO (how much data may be lost).
One line apiece: ⟦elasticity is capacity tracking demand; agility is building fast; disaster recovery is getting back after a failure⟧.

[The ability to dynamically scale the resources available to a cloud app] -> Elasticity
The key phrase is 'dynamically scale the resources'. Anything automatic and demand-driven is elasticity.

[The ability to use cloud-based backup services to restore resources in the event of an outage] -> Disaster recovery
The key words are 'outage' and 'restore'. Recovering after a failure is disaster recovery.

[The ability to quickly deploy and configure cloud-based resources as app requirements change] -> Agility
The key phrase is 'quickly deploy and configure'. This is about speed rather than amount, so it is not elasticity."""

patch(L, 426, """Question #426  ·  Topic 1  ·  DRAG DROP
Match the cloud computing benefits to the appropriate requirements.
To answer, drag the appropriate benefit from the column on the left to its requirement on the right. Each benefit may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.

Benefits：Agility ｜ Elasticity ｜ Disaster recovery

Answer Area（紅框標出的正解順序；描述裡的 [ ] 是紅框另外圈起來的關鍵字）
1. The ability to [dynamically scale] the resources available to a cloud app　→　Elasticity
2. The ability to use cloud-based backup services to restore resources in the [event of an outage]　→　Disaster recovery
3. The ability to quickly deploy and configure cloud-based resources as app [requirements change]　→　Agility

（核對來源：PDF 第 125 頁）""", line_edits=[
    (" tgt:[", ' tgt:' + arr(["能夠⟦動態調整⟧某個雲端應用程式可用的資源",
                             "能夠在⟦發生中斷事件時⟧，使用雲端的備份服務還原資源",
                             "能夠在應用程式⟦需求改變⟧時，快速部署與設定雲端資源"]) + ','),
    (" e:", ' e:' + js(E426) + ','),
    ("     tgt:[", '     tgt:' + arr(["The ability to ⟦dynamically scale⟧ the resources available to a cloud app",
                                     "The ability to use cloud-based backup services to restore resources in the ⟦event of an outage⟧",
                                     "The ability to quickly deploy and configure cloud-based resources as app ⟦requirements change⟧"]) + ','),
    ("     e:", '     e:' + js(EN426) + '}},'),
])

# ══ #427（PDF 第 125 頁）═════════════════════════════════════════════
E427 = """縱深防禦（Defense-in-Depth）把安全防護排成一層包一層的同心圓，由外而內共七層，這一題三格取了其中三層：
・⟦實體安全性（Physical security）⟧— 資料中心的門禁、警衛、監視攝影機、生物辨識。擋的是有人真的走進機房。
・⟦身分識別與存取（Identity & access）⟧— 誰能登入、能存取什麼：單一登入、多重要素驗證（MFA）、條件式存取、以角色為基礎的存取控制（RBAC）。
・⟦周邊（Perimeter）⟧— 網路邊界的防護：DDoS 防護、周邊防火牆。
・⟦網路（Network）⟧— 網路分段與流量控管：網路安全性群組（NSG）、子網路隔離、預設拒絕。
・⟦運算（Compute）⟧— 主機層的安全：⟦作業系統與應用程式的更新與修補程式⟧、端點保護、關閉不必要的連接埠。
・⟦應用程式（Application）⟧— 安全開發生命週期、弱點掃描、祕密不寫進程式碼（改放 Key Vault）。
・⟦資料（Data）⟧— 最內層：待用與傳輸中的加密、備份、資料分類與存取控管。
核心觀念：⟦任何一層都可能被突破，所以每一層都要能獨立防護，不能只靠邊界⟧。

【運算層（Compute）】→ 軟體更新與修補程式
修補程式修的是作業系統與應用程式執行所在的主機，屬於運算層。

【身分識別與存取層（Identity and access）】→ 多重要素驗證（MFA）
MFA 是在驗證「你是誰」的時候多加一道要素，明確落在身分識別與存取層。

【實體安全性層（Physical security）】→ 監視攝影機
攝影機看的是實體空間，是最外層的實體安全性。"""

EN427 = """Defense in depth arranges controls as concentric rings, seven layers from the outside in; this question takes three of them:
・⟦Physical security⟧ — datacenter access control, guards, surveillance cameras, biometrics. It stops someone physically walking into the room.
・⟦Identity & access⟧ — who may sign in and reach what: single sign-on, multifactor authentication (MFA), Conditional Access, role-based access control (RBAC).
・⟦Perimeter⟧ — protection at the network edge: DDoS protection, perimeter firewalls.
・⟦Network⟧ — segmentation and traffic control: network security groups (NSGs), subnet isolation, deny by default.
・⟦Compute⟧ — host-level security: ⟦operating system and application updates and patches⟧, endpoint protection, closing unnecessary ports.
・⟦Application⟧ — a secure development lifecycle, vulnerability scanning, and keeping secrets out of code (in Key Vault instead).
・⟦Data⟧ — the innermost ring: encryption at rest and in transit, backup, classification and access control.
The central idea: ⟦any single layer can be breached, so every layer must defend on its own rather than relying on the edge⟧.

[Compute] -> Software updates and patches
Patches fix the operating system and the host the application runs on, which is the compute layer.

[Identity and access] -> Multifactor authentication (MFA)
MFA adds a factor while proving who you are, placing it squarely in identity and access.

[Physical security] -> Surveillance camera
A camera watches physical space, which is the outermost ring."""

patch(L, 427, """Question #427  ·  Topic 1  ·  DRAG DROP
Match the security components to the appropriate defense in depth layers.
To answer, drag the appropriate security component from the column on the left to its defense in depth layer on the right Each security component may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.

Components：Multifactor authentication (MFA) ｜ Software updates and patches ｜ Surveillance camera

Answer Area（紅框標出的正解順序）
1. Compute　→　Software updates and patches
2. Identity and access　→　Multifactor authentication (MFA)
3. Physical security　→　Surveillance camera

（核對來源：PDF 第 125 頁）""", line_edits=[
    (" e:", ' e:' + js(E427) + ','),
    ("     e:", '     e:' + js(EN427) + '}},'),
])

# ══ #461（PDF 第 134 頁）═════════════════════════════════════════════
E461 = """原文的可拖曳欄有四個服務，答案區只有三格，⟦Azure 容器是沒有用到的干擾項⟧。四個一起記：
・⟦ExpressRoute⟧— 透過連線提供者拉一條⟦私人專線⟧進 Microsoft 骨幹，流量完全不經過公用網際網路。頻寬 50 Mbps 到 100 Gbps，延遲穩定並提供 SLA；適合大量資料移轉與對延遲敏感的正式環境，成本最高。
・⟦虛擬私人網路（VPN）⟧— 走公用網際網路，但用 IPsec/IKE 把流量加密，兩端各需要一個⟦閘道⟧。分站對站（S2S：地端裝置對 Azure）、點對站（P2S：單一用戶端對 Azure）與 VNet 對 VNet。建置快、便宜，但頻寬與延遲隨網際網路狀況浮動。
・⟦Azure 虛擬桌面（Azure Virtual Desktop）⟧— 在 Azure 上執行的完整桌面與應用程式虛擬化服務，支援 Windows 10／11 多工作階段與 FSLogix 使用者設定檔容器，使用者從任何裝置連進來用同一個雲端桌面。
・⟦Azure 容器（Container Instances、Container Apps、AKS）⟧— 執行容器化應用程式的運算服務，與「怎麼連線」無關，是本題的干擾項。
記法：⟦不經網際網路的專線 → ExpressRoute；用閘道加密走網際網路 → VPN；雲端桌面 → Azure 虛擬桌面⟧。

【不經過網際網路的專用私人連線】→ ExpressRoute
關鍵字是「不經過網際網路」。這是 ExpressRoute 與 VPN 最根本的差別。

【使用閘道來加密地端與 Azure 之間的流量】→ 虛擬私人網路（VPN）
關鍵字是「閘道」加「加密」。走的是公網，靠加密保護。

【提供在 Azure 上執行的完整桌面與應用程式虛擬化環境】→ Azure 虛擬桌面
關鍵字是「桌面虛擬化」。四個裡只有它是給人用的桌面服務。"""

EN461 = """The source offers four services but the answer area has three boxes — ⟦Azure containers is the unused distractor⟧. Learn all four together:
・⟦ExpressRoute⟧ — a ⟦private circuit⟧ into the Microsoft backbone through a connectivity provider, with traffic never touching the public internet. Bandwidth from 50 Mbps to 100 Gbps, predictable latency and an SLA; suited to bulk data transfer and latency-sensitive production. The most expensive option.
・⟦Virtual Private Network (VPN)⟧ — travels the public internet but encrypts traffic with IPsec/IKE, requiring a ⟦gateway⟧ at each end. Site-to-site (an on-premises device to Azure), point-to-site (a single client to Azure) and VNet-to-VNet. Quick and cheap, with bandwidth and latency at the internet's mercy.
・⟦Azure Virtual Desktop⟧ — a full desktop and application virtualization service running in Azure, with Windows 10/11 multi-session and FSLogix profile containers, letting users reach the same cloud desktop from any device.
・⟦Azure containers (Container Instances, Container Apps, AKS)⟧ — compute services for running containerised applications, unrelated to connectivity and the distractor here.
Rule of thumb: ⟦a private circuit off the internet → ExpressRoute; gateways encrypting traffic over the internet → VPN; a cloud desktop → Azure Virtual Desktop⟧.

[A dedicated private connection that does not traverse the internet] -> ExpressRoute
The key phrase is 'does not traverse the internet', the fundamental difference between ExpressRoute and VPN.

[Uses gateways to encrypt traffic between on-premises and Azure] -> Virtual Private Network (VPN)
The key words are 'gateways' and 'encrypt'. It uses the public path and relies on encryption for safety.

[Provides a full desktop and app virtualization environment that runs in Azure] -> Azure Virtual Desktop
The key phrase is desktop virtualization; it is the only one of the four that serves a person a desktop."""

patch(L, 461, """Question #461  ·  Topic 1  ·  DRAG DROP
Match the Azure compute services to the appropriate descriptions.
To answer, drag the appropriate compute service from the column on the left to its description on the right. Each service may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.

Services：Azure containers ｜ Azure Virtual Desktop ｜ ExpressRoute ｜ Virtual Private Network (VPN)

Answer Area（紅框標出的正解順序）
1. A dedicated private connection that does not traverse the internet.　→　ExpressRoute
2. Uses gateways to encrypt traffic between on-premises and Azure.　→　Virtual Private Network (VPN)
3. Provides a full desktop and app virtualization environment that runs in Azure.　→　Azure Virtual Desktop

（核對來源：PDF 第 134 頁。Azure containers 是沒有用到的干擾項）""", line_edits=[
    (" e:", ' e:' + js(E461) + ','),
    ("     tgt:[", '     tgt:' + arr(["⟦A dedicated private connection that does not traverse the internet⟧",
                                     "⟦Uses gateways to encrypt traffic between on-premises and Azure⟧",
                                     "⟦Provides a full desktop and app virtualization environment that runs in Azure⟧"]) + ','),
    ("     e:", '     e:' + js(EN461) + '}},'),
])

# ══ #464（PDF 第 135 頁）═════════════════════════════════════════════
# 原文兩個下拉的選項順序都是 Monitor / Subscriptions / Marketplace / Advisor，
# 反推版本把第二格的正解搬到第一個；改回原文順序並重對 a。
BLADES = ["監視器（Monitor）", "訂用帳戶（Subscriptions）", "市集（Marketplace）", "顧問（Advisor）"]
BLADES_EN = ["Monitor", "Subscriptions", "Marketplace", "Advisor"]

E464 = """Azure 入口網站幾個刀鋒視窗的分工：
・⟦監視器（Monitor）⟧— 計量、記錄與警示的總入口；底下含 Application Insights（應用程式）、Log Analytics（記錄查詢）與服務健康狀態（Azure 服務本身的中斷、計畫維護與健康狀況建議）。要看「Azure 服務健不健康」就從這裡進去。
・⟦顧問（Advisor）⟧— 個人化建議，分可靠性、安全性、效能、成本、卓越營運五類。其中的安全性建議來自 Microsoft Defender for Cloud，在顧問裡一起呈現。
・⟦市集（Marketplace）⟧— 第一方與第三方的映像、虛擬設備與解決方案目錄；入口網站左側的「建立資源」就是它。本題的干擾項。
・⟦訂用帳戶（Subscriptions）⟧— 訂用帳戶清單、計費、資源計數與存取控制，與這兩件工作都無關，也是干擾項。
本題與 #171 是同一組題目，#171 多了「瀏覽可用的虛擬機器映像 → 市集」那一格。

【監視 Azure 服務的健康狀態】→ 監視器（Monitor）
注意是「Azure 服務」的健康狀態，不是你自己應用程式的健康狀態；前者在監視器底下的服務健康狀態，後者才是 Application Insights。

【檢視安全性建議】→ 顧問（Advisor）
「建議」兩個字直接指向顧問。安全性建議是它五類建議中的一類。"""

EN464 = """How the Azure portal blades divide the work:
・⟦Monitor⟧ — the front door for metrics, logs and alerts, with Application Insights (applications), Log Analytics (log queries) and Service Health (outages, planned maintenance and health advisories for Azure itself) underneath it. 'Is the Azure service healthy' starts here.
・⟦Advisor⟧ — personalised recommendations across reliability, security, performance, cost and operational excellence. The security ones come from Microsoft Defender for Cloud and are surfaced here with the rest.
・⟦Marketplace⟧ — the catalogue of first- and third-party images, appliances and solutions; the portal's 'Create a resource' button is this. A distractor here.
・⟦Subscriptions⟧ — the subscription list, billing, resource counts and access control. Unrelated to either task and the other distractor.
This is the same question as #171, which adds a third box, 'Browse available virtual machine images → Marketplace'.

[Monitor the health of Azure services] -> Monitor
Note that this is the health of the Azure services, not of your own application: the former is Service Health under Monitor, the latter is Application Insights.

[View security recommendations] -> Advisor
The word 'recommendations' points straight at Advisor; security is one of its five categories."""

patch(L, 464, """Question #464  ·  Topic 1  ·  HOTSPOT
You need to identify which blades in the Azure portal must be used to perform the following tasks:
・View security recommendations.
・Monitor the health of Azure services.
Which blade should you identify for each task? To answer, select the appropriate options in the answer area.
NOTE: Each correct selection is worth one point.

Answer Area（兩個下拉的選項都是 Monitor ｜ Subscriptions ｜ Marketplace ｜ Advisor）
1. Monitor the health of Azure services:　→　Monitor
2. View security recommendations:　→　Advisor

（核對來源：PDF 第 135 頁。本題與 #171 是同一組題目，#171 多一格「瀏覽虛擬機器映像」）""", line_edits=[
    (" q:", ' q:' + js("你要找出在 Azure 入口網站裡，執行下列工作各該使用哪一個刀鋒視窗（blade）：\n"
                       "・檢視安全性建議。\n・監視 Azure 服務的健康狀態。\n"
                       "每一項工作各該選哪一個刀鋒視窗？請在答案區選出正確的選項。") + ','),
    (" dd:[", ' dd:' + arr2([BLADES, BLADES]) + ','),
    (" a:[", ' a:[0,3],'),
    (" e:", ' e:' + js(E464) + ','),
    (" en:{q:", ' en:{q:' + js("You need to identify which blades in the Azure portal must be used to perform the following tasks:\n"
                               "・View security recommendations.\n・Monitor the health of Azure services.\n"
                               "Which blade should you identify for each task? To answer, select the appropriate options in the answer area.") + ','),
    ("     dd:[", '     dd:' + arr2([BLADES_EN, BLADES_EN]) + ','),
    ("     e:", '     e:' + js(EN464) + '}},'),
])

# #171 的 Advisor 中譯統一成「顧問」，並補註與 #464 是同一組題目
patch(L, 171, None, text_subs=[("建議程式", "顧問")])

# ══ #469（PDF 第 137 頁）═════════════════════════════════════════════
E469 = """三種驗證方式在「安全性」與「便利性」兩個軸上的位置（原題的答案區就是一張四象限圖）：
・⟦密碼驗證（Password authentication）⟧— 只靠「你知道的」一個要素。使用者會重複使用、寫在便條紙上、選容易猜的字串，因此會被網路釣魚、暴力破解與憑證填充攻破。⟦安全性低、便利性高⟧。
・⟦多重要素驗證（MFA）⟧— 密碼之外再加一個不同類別的要素：你擁有的（手機驗證碼、驗證器 App、FIDO2 硬體金鑰）或你本身的（指紋、臉部）。安全性大幅提升（Microsoft 統計可擋下 99.9% 以上的帳戶入侵），但每次登入都多一道手續。⟦安全性高、便利性低⟧。
・⟦無密碼驗證（Passwordless）⟧— 直接把密碼拿掉，改用 Windows Hello for Business、FIDO2 安全金鑰或 Microsoft Authenticator 的手機登入。本質上仍然是多重要素（裝置 + 生物特徵或 PIN），但使用者只需要一個動作。⟦安全性高、便利性也高⟧，是 Microsoft 目前主推的方向。
記法：⟦密碼方便但不安全；MFA 安全但麻煩；無密碼兩者兼得⟧。

【安全性高，但便利性低】→ 多重要素驗證（MFA）
安全性靠的是「多一個要素」，代價就是使用者每次登入都要多做一件事。

【安全性高，而且便利性也高】→ 無密碼驗證
拿掉最脆弱的環節（密碼），同時把要素收進使用者本來就帶著的裝置與生物特徵裡。

【安全性低，但便利性高】→ 密碼驗證
只要記得起來就能用，這是它唯一的優點，也是它所有問題的來源。"""

EN469 = """Where the three authentication methods sit on the security and convenience axes (the answer area in the source is a four-quadrant chart):
・⟦Password authentication⟧ — a single factor, something you know. People reuse passwords, write them down and pick guessable ones, so phishing, brute force and credential stuffing all work. ⟦Low security, high convenience⟧.
・⟦Multifactor authentication (MFA)⟧ — a password plus a factor from another category: something you have (a code, an authenticator app, a FIDO2 key) or something you are (fingerprint, face). Security improves dramatically — Microsoft measures it as blocking over 99.9% of account compromise — at the cost of an extra step on every sign-in. ⟦High security, inconvenient⟧.
・⟦Passwordless authentication⟧ — removes the password entirely in favour of Windows Hello for Business, a FIDO2 security key or phone sign-in through Microsoft Authenticator. It is still multifactor underneath (a device plus a biometric or PIN), but the user performs one action. ⟦High security and convenient⟧, and where Microsoft is steering everyone.
One line apiece: ⟦passwords are convenient but weak; MFA is strong but tedious; passwordless is both⟧.

[High security but inconvenient] -> Multifactor authentication (MFA)
The strength comes from the extra factor, and the extra factor is exactly what costs the user an extra step.

[High security and convenient] -> Passwordless authentication
It removes the weakest link and folds the factors into the device and biometric the user already carries.

[Low security but convenient] -> Password authentication
If you can remember it you can use it — its only virtue, and the source of all its problems."""

patch(L, 469, """Question #469  ·  Topic 1  ·  DRAG DROP
Match the authentication method to the appropriate level of security.
To answer, drag the appropriate authentication method from the column on the left to its level of security on the right.
NOTE: Each correct match is worth one point.

Authentication methods：Multifactor authentication (MFA) ｜ Password authentication ｜ Passwordless authentication

Answer Area 是一張四象限圖，縱軸 High Security ↑ / Low Security ↓，橫軸 Inconvenient ← / Convenient →。
紅框標出的正解位置
1. 左上（高安全性、不便利）　→　Multifactor authentication (MFA)
2. 右上（高安全性、便利）　→　Passwordless authentication
3. 右下（低安全性、便利）　→　Password authentication

（核對來源：PDF 第 137 頁。原題是四象限圖，這裡改寫成三格文字描述）""", line_edits=[
    (" q:", ' q:' + js("（原題的答案區是一張四象限圖，縱軸是安全性高低、橫軸是便利與否；這裡改寫成逐格的文字描述。）\n"
                       "請把左邊的驗證方式拖曳到右邊對應的安全性／便利性象限上。") + ','),
    (" e:", ' e:' + js(E469) + ','),
    (" en:{q:", ' en:{q:' + js("(In the source the answer area is a four-quadrant chart, security on the vertical axis and convenience on the horizontal; each quadrant is written out here.)\n"
                               "Drag each authentication method on the left to the matching security and convenience quadrant on the right.") + ','),
    ("     tgt:[", '     tgt:' + arr(["⟦High security but inconvenient⟧", "⟦High security and convenient⟧", "⟦Low security but convenient⟧"]) + ','),
    ("     e:", '     e:' + js(EN469) + '}},'),
])

# ══ #472（PDF 第 138 頁）═════════════════════════════════════════════
E472 = """三種雲端服務模型的控制權由多到少：
・⟦基礎結構即服務（IaaS）⟧— 拿到虛擬機器、虛擬網路、磁碟這類基礎資源。作業系統、修補、防毒、中介軟體、執行階段、應用程式與資料全部歸你，⟦對雲端環境的控制權最大⟧，管理負擔也最重。Azure 虛擬機器就是跑在 IaaS 上的。
・⟦平台即服務（PaaS）⟧— 雲端商接手作業系統與執行階段，你只管應用程式與資料。以資料庫為例，Azure SQL Database 讓你完全掌控資料庫設計（結構描述、索引、預存程序、效能調整），但⟦不必維護底下的作業系統⟧。
・⟦軟體即服務（SaaS）⟧— 連應用程式都由雲端商提供與維運，你只管自己的資料、帳號與存取設定。控制權最小、管理負擔最輕，代表是 Microsoft 365 與 Dynamics 365。
最後提醒共同責任模型的鐵則：⟦不論哪一種服務模型，資料與身分識別／帳號的責任永遠在客戶身上，這一點永遠不會轉移⟧。

【對雲端環境提供最大的控制權】→ 基礎結構即服務（IaaS）
控制權與管理負擔是同一件事的兩面：管得最多的就是控制得最多的。

【在不必維護作業系統的前提下，對資料庫設計提供最大的控制權】→ 平台即服務（PaaS）
這一格的關鍵是「不必維護作業系統」。同樣能完全掌控資料庫設計，但作業系統交給平台，那就是 PaaS。

【用來裝載（host）Azure 虛擬機器】→ 基礎結構即服務（IaaS）
虛擬機器本身就是 IaaS 的產物。注意這一題允許同一個項目用兩次，IaaS 出現了兩格。"""

EN472 = """The three service models ranked by how much control you keep:
・⟦Infrastructure as a service (IaaS)⟧ — you get base resources: virtual machines, virtual networks, disks. The OS, patching, antivirus, middleware, runtime, application and data are all yours, giving ⟦the most control of the cloud environment⟧ and the heaviest management burden. Azure virtual machines run on IaaS.
・⟦Platform as a service (PaaS)⟧ — the provider takes the OS and runtime; you keep the application and its data. With databases, Azure SQL Database gives you full control of the database design (schema, indexes, stored procedures, tuning) ⟦without maintaining the operating system underneath⟧.
・⟦Software as a service (SaaS)⟧ — even the application is supplied and operated by the provider; you keep only your data, accounts and access settings. The least control and the lightest burden, as with Microsoft 365 and Dynamics 365.
And the standing rule of the shared responsibility model: ⟦whatever the service model, responsibility for data and for identities and accounts always stays with the customer, and never transfers⟧.

[Provides the most control of a cloud environment] -> Infrastructure as a service (IaaS)
Control and management burden are two sides of one coin: whoever manages the most controls the most.

[Provides the most control of a database design without having to maintain the operating system] -> Platform as a service (PaaS)
The decisive phrase is 'without having to maintain the operating system'. Full control of the database design but no OS to keep means PaaS.

[Used to host Azure virtual machines] -> Infrastructure as a service (IaaS)
A virtual machine is the definitive IaaS artifact. Note that this question lets one item be used twice, and IaaS fills two of the boxes."""

patch(L, 472, """Question #472  ·  Topic 1  ·  DRAG DROP
Match the cloud service to the appropriate description.
To answer, drag the appropriate cloud service from the column on the left to its description on the right. Each service may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.

Cloud services：Infrastructure as a service (IaaS) ｜ Platform as a service (PaaS) ｜ Software as a service (SaaS)

Answer Area（紅框標出的正解順序；IaaS 用了兩次）
1. Provides the most control of a cloud environment.　→　Infrastructure as a service (IaaS)
2. Provides the most control of a database design without having to maintain the operating system.　→　Platform as a service (PaaS)
3. Used to host Azure virtual machines.　→　Infrastructure as a service (IaaS)

（核對來源：PDF 第 138 頁）""", line_edits=[
    (" e:", ' e:' + js(E472) + ','),
    ("     tgt:[", '     tgt:' + arr(["⟦Provides the most control of a cloud environment⟧",
                                     "⟦Provides the most control of a database design without having to maintain the operating system⟧",
                                     "⟦Used to host Azure virtual machines⟧"]) + ','),
    ("     e:", '     e:' + js(EN472) + '}},'),
])

save(L)
print("批次 F 完成：#426 #427 #461 #464 #469 #472（並統一 #171 的 Advisor 中譯）")
