# -*- coding: utf-8 -*-
"""核對原文 批次 E：#249 #272 #287 #386 #387 #395（PDF 第 74、80、85、113、116 頁）。
   同時把解析改寫成「共用對照一次 + 逐格重點」。一次性腳本，保留供追溯。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vfy import load, save, patch, js, arr, arr2

L = load()

# ══ #249（PDF 第 74 頁）══════════════════════════════════════════════
# 原文兩個下拉的選項順序相同（Azure Monitor / Azure Security Center /
# Azure AD Identity Protection / Azure ATP），反推版本把正解搬到各格第一個；
# 服務名稱也照原文用當年的舊名。
SEC249 = ["Azure 監視器（Azure Monitor）",
          "Azure 資訊安全中心（Azure Security Center）",
          "Azure Active Directory（Azure AD）Identity Protection",
          "Azure 進階威脅防護（Azure Advanced Threat Protection, ATP）"]
SEC249_EN = ["Azure Monitor",
             "Azure Security Center",
             "Azure Active Directory (Azure AD) Identity Protection",
             "Azure Advanced Threat Protection (ATP)"]

E249 = """四個安全性服務的分工，一次分清楚：
・⟦Azure 進階威脅防護（Azure ATP，現稱 Microsoft Defender for Identity）⟧— 在地端網域控制站上安裝⟦感應器（sensor）⟧，直接讀取網域控制站的流量與 Windows 事件，偵測針對 Active Directory 的攻擊：帳戶列舉、Pass-the-Hash、Pass-the-Ticket、黃金票證、DCSync、橫向移動路徑。「用感應器監視威脅」指的就是它。
・⟦Azure AD Identity Protection（現稱 Microsoft Entra ID Protection）⟧— 用機器學習替每一次登入與每一個使用者算出⟦風險等級⟧（不可能的移動、匿名 IP 位址、外洩的認證、異常登入位置），再依風險自動套用原則：要求 MFA、強制變更密碼或直接封鎖存取。
・⟦Azure 資訊安全中心（Azure Security Center，現稱 Microsoft Defender for Cloud）⟧— 雲端安全狀態管理與工作負載保護：安全分數、法規遵循儀表板、強化建議、JIT 虛擬機器存取。它看的是資源的設定，不是身分。
・⟦Azure 監視器（Azure Monitor）⟧— 通用的計量、記錄與警示平台。它什麼都能收，但不是專門的威脅偵測服務。
名稱對照（考題常用舊名）：⟦Azure ATP → Defender for Identity；Azure Security Center → Defender for Cloud；Azure AD → Microsoft Entra ID⟧。

【用感應器監視威脅】→ Azure 進階威脅防護（ATP）
關鍵字是「感應器」。四個服務裡只有 ATP 需要在網域控制站上裝感應器，其餘三個都是純雲端服務。

【依條件強制執行 Azure 多重要素驗證（MFA）】→ Azure AD Identity Protection
關鍵字是「依條件」。依風險條件自動要求 MFA，是 Identity Protection 的風險原則（與條件式存取搭配）做的事；若題目只說「一律要求 MFA」，那就是單純的條件式存取。"""

EN249 = """Separate the four security services once:
・⟦Azure Advanced Threat Protection (Azure ATP, now Microsoft Defender for Identity)⟧ — a ⟦sensor⟧ installed on on-premises domain controllers reads controller traffic and Windows events directly to detect attacks against Active Directory: account enumeration, Pass-the-Hash, Pass-the-Ticket, golden ticket, DCSync, lateral movement paths. 'Monitor threats by using sensors' means this.
・⟦Azure AD Identity Protection (now Microsoft Entra ID Protection)⟧ — machine learning assigns a ⟦risk level⟧ to every sign-in and every user (impossible travel, anonymous IP address, leaked credentials, unfamiliar sign-in properties), then policy acts on that risk automatically: require MFA, force a password change, or block access.
・⟦Azure Security Center (now Microsoft Defender for Cloud)⟧ — cloud security posture management and workload protection: secure score, regulatory compliance dashboard, hardening recommendations, just-in-time VM access. It looks at resource configuration, not identity.
・⟦Azure Monitor⟧ — the general metrics, logs and alerting platform. It can collect almost anything, but it is not a dedicated threat detection service.
Name changes (exams still use the old ones): ⟦Azure ATP → Defender for Identity; Azure Security Center → Defender for Cloud; Azure AD → Microsoft Entra ID⟧.

[Monitor threats by using sensors] -> Azure Advanced Threat Protection (ATP)
The key word is sensors. Of the four, only ATP installs a sensor on domain controllers; the other three are pure cloud services.

[Enforce Azure MFA based on a condition] -> Azure Active Directory (Azure AD) Identity Protection
The key phrase is 'based on a condition'. Requiring MFA automatically in response to risk is what Identity Protection's risk policies do, working with Conditional Access. A question that simply says 'always require MFA' would be plain Conditional Access."""

patch(L, 249, """Question #249  ·  Topic 1  ·  HOTSPOT
You plan to implement several security services for an Azure environment. You need to identify which Azure services must be used to meet the following security requirements:
➯ Monitor threats by using sensors
➯ Enforce Azure Multi-Factor Authentication (MFA) based on a condition
Which Azure service should you identify for each requirement? To answer, select the appropriate options in the answer area.
NOTE: Each correct selection is worth one point.
Hot Area:

Answer Area（兩個下拉的選項相同，順序如下）
Azure Monitor ｜ Azure Security Center ｜ Azure Active Directory (Azure AD) Identity Protection ｜ Azure Advanced Threat Protection (ATP)

紅框標出的正解
1. Monitor threats by using sensors:　→　Azure Advanced Threat Protection (ATP)
2. Enforce Azure MFA based on a condition:　→　Azure Active Directory (Azure AD) Identity Protection

（核對來源：PDF 第 74 頁。服務名稱照原文的舊稱，現行名稱見解析）""", line_edits=[
    (" q:", ' q:' + js("你打算替 Azure 環境實作數項安全性服務，並要找出下列每一項安全性需求各該使用哪一個 Azure 服務：\n"
                       "・用感應器監視威脅\n・依條件強制執行 Azure 多重要素驗證（MFA）\n"
                       "每一項需求各該選出哪一個 Azure 服務？請在答案區選出正確的選項。") + ','),
    (" dd:[", ' dd:' + arr2([SEC249, SEC249]) + ','),
    (" a:[", ' a:[3,2],'),
    (" e:", ' e:' + js(E249) + ','),
    (" en:{q:", ' en:{q:' + js("You plan to implement several security services for an Azure environment. You need to identify which Azure services must be used to meet the following security requirements:\n"
                               "・Monitor threats by using sensors\n・Enforce Azure Multi-Factor Authentication (MFA) based on a condition\n"
                               "Which Azure service should you identify for each requirement? To answer, select the appropriate options in the answer area.") + ','),
    ("     dd:[", '     dd:' + arr2([SEC249_EN, SEC249_EN]) + ','),
    ("     e:", '     e:' + js(EN249) + '}},'),
])

# ══ #272（PDF 第 80 頁）══════════════════════════════════════════════
E272 = """四個名詞分屬三種性質：標準組織、法規、雲端環境。一次分清楚：
・⟦ISO（國際標準化組織）⟧— 跨所有產業的國際標準制定者。與 Azure 有關的常考標準：ISO/IEC 27001（資訊安全管理系統）、27017（雲端服務資訊安全控制）、27018（雲端個人資料保護）、9001（品質管理）。
・⟦NIST（美國國家標準暨技術研究院）⟧— 美國商務部底下的機構，制定美國聯邦政府使用的標準：NIST SP 800-53（聯邦資訊系統的控制措施）、NIST 網路安全架構（CSF）、FIPS 140-2（加密模組驗證）。
・⟦GDPR（一般資料保護規範）⟧— 歐盟 2018 年生效的資料隱私與資料保護法規，賦予當事人存取、更正、刪除（被遺忘權）與資料可攜等權利。只要處理歐盟居民的個人資料就適用，不論公司設在哪裡；違規最高可罰全球年營業額的 4%。
・⟦Azure Government⟧— 專供美國聯邦、州與地方政府機構及其合作夥伴使用的⟦實體隔離⟧雲端執行個體，由通過審查的美國公民營運，符合 FedRAMP High、DoD IL5、CJIS、ITAR 等要求。它是獨立的雲端，不是 Azure 全球版的一項功能。
記法：⟦ISO 是國際的標準組織、NIST 是美國政府的標準組織、GDPR 是歐盟的法規、Azure Government 是美國政府專用的雲⟧。

【定義適用於所有產業之國際標準的組織】→ ISO
關鍵字是「國際」加「所有產業」。ISO 的標準不限產業也不限國家。

【定義美國政府所使用之標準的組織】→ NIST
關鍵字是「美國政府」。NIST 與 ISO 都是標準組織，差別在服務對象。

【規範資料隱私與資料保護的歐盟政策】→ GDPR
關鍵字是「歐盟」加「資料隱私」。四個裡只有 GDPR 是法規而不是組織或雲端。

【專供美國聯邦與州政府機構使用的專用公有雲】→ Azure Government
關鍵字是「專用的雲」。它是一個獨立的 Azure 執行個體，與 Azure 全球版實體隔離。"""

EN272 = """The four terms fall into three kinds of thing: standards bodies, regulation, and a cloud environment. Separate them once:
・⟦ISO (International Organization for Standardization)⟧ — sets international standards across every industry. The ones that come up with Azure: ISO/IEC 27001 (information security management), 27017 (cloud service security controls), 27018 (personal data in the cloud), 9001 (quality management).
・⟦NIST (National Institute of Standards and Technology)⟧ — an agency of the US Department of Commerce that sets the standards used by the US federal government: NIST SP 800-53 (controls for federal information systems), the NIST Cybersecurity Framework (CSF), FIPS 140-2 (cryptographic module validation).
・⟦GDPR (General Data Protection Regulation)⟧ — the EU data privacy and protection regulation in force since 2018, granting rights of access, rectification, erasure (the right to be forgotten) and portability. It applies to anyone processing the personal data of EU residents regardless of where the company sits, with fines up to 4% of global annual turnover.
・⟦Azure Government⟧ — a ⟦physically isolated⟧ instance of the cloud for US federal, state and local agencies and their partners, operated by screened US citizens, meeting FedRAMP High, DoD IL5, CJIS and ITAR requirements. It is a separate cloud, not a feature of global Azure.
Rule of thumb: ⟦ISO is the international standards body, NIST the US government's, GDPR the EU's regulation, and Azure Government the US government's own cloud⟧.

[An organization that defines international standards across all industries] -> ISO
The key words are international and all industries. ISO standards are bound to neither a sector nor a country.

[An organization that defines standards used by the United States government] -> NIST
The key phrase is 'United States government'. NIST and ISO are both standards bodies; the difference is who they serve.

[A European policy that regulates data privacy and data protection] -> GDPR
The key words are European and data privacy. Of the four, only GDPR is a regulation rather than an organisation or a cloud.

[A dedicated public cloud for federal and state agencies in the United States] -> Azure Government
The key word is dedicated. It is a separate Azure instance, physically isolated from global Azure."""

patch(L, 272, """Question #272  ·  Topic 1  ·  DRAG DROP
Match the term to the correct definition.
Instructions: To answer, drag the appropriate term from the column on the left to its description on the right. Each term may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.
Select and Place:

Answer Options：Azure Government ｜ GDPR ｜ ISO ｜ NIST

Answer Area（紅框標出的正解順序；描述裡的 [ ] 是紅框另外圈起來的關鍵字）
1. An organization that defines international standards [across all industries.]　→　ISO
2. An organization that defines standards used by the [United States government.]　→　NIST
3. A [European] policy that regulates data privacy and data protection.　→　GDPR
4. A dedicated [public cloud] for federal and state agencies in the United States.　→　Azure Government

（核對來源：PDF 第 80 頁）""", line_edits=[
    (" tgt:[", ' tgt:' + arr(["定義⟦適用於所有產業⟧之國際標準的組織",
                             "定義⟦美國政府⟧所使用之標準的組織",
                             "規範資料隱私與資料保護的⟦歐盟⟧政策",
                             "專供美國聯邦與州政府機構使用的專用⟦公有雲⟧"]) + ','),
    (" e:", ' e:' + js(E272) + ','),
    ("     tgt:[", '     tgt:' + arr(["An organization that defines international standards ⟦across all industries⟧",
                                     "An organization that defines standards used by the ⟦United States government⟧",
                                     "A ⟦European⟧ policy that regulates data privacy and data protection",
                                     "A dedicated ⟦public cloud⟧ for federal and state agencies in the United States"]) + ','),
    ("     e:", '     e:' + js(EN272) + '}},'),
])

# ══ #287（PDF 第 85 頁）══════════════════════════════════════════════
E287 = """三份文件的性質與用途，一次分清楚：
・⟦Microsoft 隱私權聲明（Privacy Statement）⟧— 對所有人公開的說明性文件：Microsoft 蒐集哪些個人資料、怎麼蒐集、如何使用、與誰分享，以及你可以怎麼檢視與管理自己的資料。它不是合約。
・⟦資料保護附錄（Data Protection Addendum, DPA）⟧— 有法律約束力的合約附錄，訂明 Microsoft 與客戶雙方對客戶資料與個人資料在處理與安全性上各自的義務，含 GDPR 要求的資料處理者條款、標準契約條款與安全性措施承諾。
・⟦線上服務條款（Online Services Terms, OST）⟧— 授權與使用條款文件，定義線上服務的資料處理與安全性條款，包含已處理資料的揭露，以及資料的移轉、保留與刪除。
常一起考的兩個入口也順便記：⟦Microsoft 信任中心（Trust Center）⟧是講隱私、安全性與法規遵循的資訊入口；⟦服務信任入口網站（Service Trust Portal）⟧放的是實際的稽核報告與法規遵循文件。
一句話分：⟦隱私權聲明＝說明蒐集了什麼；DPA＝雙方的法律義務；OST＝線上服務的資料處理與安全性條款⟧。

【說明蒐集了哪些個人資料、資料如何被使用，以及這些資料的用途】→ Microsoft 隱私權聲明
關鍵字是「說明」。它是公開說明，不涉及雙方義務。

【法律協議，詳述 Microsoft 與客戶之間對客戶資料及個人資料的處理與安全性所負的義務】→ 資料保護附錄
關鍵字是「法律協議」加「義務」。三份裡只有 DPA 明講是雙方之間的合約。

【定義線上服務的資料處理與安全性條款，包含已處理資料的揭露，以及資料的移轉、保留與刪除】→ 線上服務條款
關鍵字是「線上服務」。條款的範圍綁在服務上，而不是綁在某一位客戶身上。"""

EN287 = """What each of the three documents is for, once:
・⟦Microsoft Privacy Statement⟧ — a public explanatory document for everyone: what personal data Microsoft collects, how it is collected, how it is used, who it is shared with, and how you can review and manage your own data. It is not a contract.
・⟦Data Protection Addendum (DPA)⟧ — a legally binding contractual addendum setting out what Microsoft and the customer each owe regarding the processing and security of customer data and personal data, including the processor terms GDPR requires, standard contractual clauses and security commitments.
・⟦Online Services Terms (OST)⟧ — the licensing and use terms document, defining the data processing and security terms for online services, including disclosure of processed data and the transfer, retention and deletion of data.
Two portals often tested alongside them: the ⟦Microsoft Trust Center⟧ is the information hub for privacy, security and compliance, while the ⟦Service Trust Portal⟧ holds the actual audit reports and compliance documents.
One line apiece: ⟦the Privacy Statement says what is collected; the DPA states each side's legal obligations; the OST defines data processing and security terms for the online services⟧.

[Describes which personal data is collected, how the data is used, and what the data is used for] -> Microsoft Privacy Statement
The key word is 'describes'. It explains publicly and creates no obligations between parties.

[A legal agreement that details the obligations between Microsoft and a customer regarding the processing and security of customer data and personal data] -> Data Protection Addendum
The key words are 'legal agreement' and 'obligations'. Only the DPA is stated to be a contract between the two sides.

[Defines the data processing and security terms for online services, including the disclosure of processed data and the transfer, retention, and deletion of data] -> Online Services Terms
The key phrase is 'online services'. The terms attach to the services rather than to any one customer."""

patch(L, 287, """Question #287  ·  Topic 1  ·  DRAG DROP
Match the resources to the appropriate descriptions.
To answer, drag the appropriate resource from the column on the left to its description on the right. Each resource may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.
Select and Place:

Resources：Data Protection Addendum ｜ Microsoft Privacy Statement ｜ Online Services Terms

Answer Area（紅框標出的正解順序；描述裡的 [ ] 是紅框另外圈起來的關鍵字）
1. Describes [which personal data is collected, how the data is used,] and what the data is used for.　→　Microsoft Privacy Statement
2. A legal agreement that details the obligations between Microsoft and a customer regarding the [processing and security of customer data and personal data.]　→　Data Protection Addendum
3. Defines the data processing and security terms for [online services,] including the disclosure of processed data and the transfer, retention, and deletion of data.　→　Online Services Terms

（核對來源：PDF 第 85 頁）""", line_edits=[
    (" tgt:[", ' tgt:' + arr(["說明⟦蒐集了哪些個人資料、資料如何被使用⟧，以及這些資料的用途",
                             "法律協議，詳述 Microsoft 與客戶之間對⟦客戶資料及個人資料的處理與安全性⟧所負的義務",
                             "定義⟦線上服務⟧的資料處理與安全性條款，包含已處理資料的揭露，以及資料的移轉、保留與刪除"]) + ','),
    (" e:", ' e:' + js(E287) + ','),
    ("     tgt:[", '     tgt:' + arr(["Describes ⟦which personal data is collected, how the data is used⟧, and what the data is used for",
                                     "A legal agreement that details the obligations between Microsoft and a customer regarding the ⟦processing and security of customer data and personal data⟧",
                                     "Defines the data processing and security terms for ⟦online services⟧, including the disclosure of processed data and the transfer, retention, and deletion of data"]) + ','),
    ("     e:", '     e:' + js(EN287) + '}},'),
])

# ══ #386（PDF 第 113 頁）═════════════════════════════════════════════
E386 = """可拖曳欄有四個效益，答案區只有三格，⟦災難復原是沒有用到的干擾項⟧。四個一起記：
・⟦高可用性（High availability）⟧— 元件失效時服務仍然持續可用。做法是備援加自動容錯移轉：可用性設定組、可用性區域、負載平衡器、多執行個體。談的是「不要中斷」。
・⟦災難復原（Disaster recovery）⟧— 整個站台或區域毀掉之後，把服務在別的地方復原起來。談的是「壞掉之後救得回來」，兩個關鍵指標是 RTO（多久之內要恢復）與 RPO（最多能接受掉多少資料）。工具是 Azure Site Recovery 與異地備援備份。
・⟦地理分散（Geo-distribution）⟧— 把應用程式與資料部署到靠近使用者的多個區域，降低延遲、改善在地體驗，也能滿足資料落地的法規要求。
・⟦可擴縮性（Scalability）⟧— 依需求增減資源。垂直擴充（scale up：換更大的規格，替虛擬機器加 RAM 或 CPU）與水平擴充（scale out：增加執行個體數量）。
最容易混淆的是前兩個：⟦高可用性是「不要倒」，災難復原是「倒了之後怎麼站起來」⟧。

【在資源失效時，提供不中斷的使用者體驗】→ 高可用性
關鍵字是「不中斷」。使用者根本不該察覺有東西壞掉，這是高可用性；若是「壞掉之後復原」才是災難復原。

【把應用程式與資料部署到鄰近使用者的區域資料中心】→ 地理分散
關鍵字是「鄰近使用者」。目的是縮短距離、降低延遲。

【可以透過替虛擬機器新增 RAM 或 CPU，動態提高運算容量】→ 可擴縮性
關鍵字是「加 RAM 或 CPU」，這正是垂直擴充，屬於可擴縮性。"""

EN386 = """Four benefits are offered but only three boxes exist — ⟦disaster recovery is the unused distractor⟧. Learn all four together:
・⟦High availability⟧ — the service keeps running when a component fails, through redundancy and automatic failover: availability sets, availability zones, load balancers, multiple instances. It is about not going down.
・⟦Disaster recovery⟧ — bringing the service back somewhere else after a whole site or region is lost. It is about getting back up, measured by RTO (how quickly service must return) and RPO (how much data may be lost). The tools are Azure Site Recovery and geo-redundant backup.
・⟦Geo-distribution⟧ — deploying apps and data to several regions near the users, cutting latency, improving the local experience and satisfying data residency rules.
・⟦Scalability⟧ — adding and removing resources with demand, either vertically (scale up: a larger size, more RAM or CPU on a VM) or horizontally (scale out: more instances).
The first two are the ones people confuse: ⟦high availability is 'do not fall over'; disaster recovery is 'how to get back up after falling over'⟧.

[Provide a continuous user experience in the event of a resource failure] -> High availability
The key word is continuous. Users should never notice that something broke; recovering after the fact would be disaster recovery.

[Deploy apps and data to regional data centers that are located close to users] -> Geo-distribution
The key phrase is 'close to users' — the whole point is shortening the distance and the latency.

[Compute capacity can be increased dynamically by adding RAM or CPU to a virtual machine] -> Scalability
The key phrase is 'adding RAM or CPU', which is scaling up, a form of scalability."""

patch(L, 386, """Question #386  ·  Topic 1  ·  DRAG DROP
Match the cloud computing benefits to the appropriate requirements.
To answer, drag the appropriate benefit from the column on the left to its requirement on the right. Each benefit may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.

Benefits：Disaster recovery ｜ Geo-distribution ｜ High availability ｜ Scalability

Answer Area（紅框標出的正解順序）
1. Provide a continuous user experience in the event of a resource failure.　→　High availability
2. Deploy apps and data to regional data centers that are located close to users.　→　Geo-distribution
3. Compute capacity can be increased dynamically by adding RAM or CPU to a virtual machine.　→　Scalability

（核對來源：PDF 第 113 頁。Disaster recovery 是沒有用到的干擾項）""", line_edits=[
    (" tgt:[", ' tgt:' + arr(["⟦在資源失效時，提供不中斷的使用者體驗⟧",
                             "⟦把應用程式與資料部署到鄰近使用者的區域資料中心⟧",
                             "⟦可以透過替虛擬機器新增 RAM 或 CPU，動態提高運算容量⟧"]) + ','),
    (" e:", ' e:' + js(E386) + ','),
    ("     tgt:[", '     tgt:' + arr(["⟦Provide a continuous user experience in the event of a resource failure⟧",
                                     "⟦Deploy apps and data to regional data centers that are located close to users⟧",
                                     "⟦Compute capacity can be increased dynamically by adding RAM or CPU to a virtual machine⟧"]) + ','),
    ("     e:", '     e:' + js(EN386) + '}},'),
])

# ══ #387（PDF 第 113 頁）═════════════════════════════════════════════
E387 = """三種連線方式一次分清楚：
・⟦ExpressRoute⟧— 透過連線提供者拉一條⟦私人專線⟧進 Microsoft 的骨幹網路，流量完全不經過公用網際網路。頻寬 50 Mbps 到 100 Gbps，延遲穩定並提供 SLA；適合大量資料移轉、混合式正式環境與對延遲敏感的應用。三種模型：CloudExchange 共置、點對點乙太網路、任意對任意（IPVPN）。成本最高。
・⟦VPN 閘道（VPN gateway）⟧— 走⟦公用網際網路⟧但把流量加密（IPsec/IKE）。分站對站（S2S：地端 VPN 裝置對 Azure）、點對站（P2S：單一用戶端裝置對 Azure）與 VNet 對 VNet。建置快、便宜，但頻寬與延遲受網際網路狀況影響。
・⟦虛擬網路對等互連（VNet peering）⟧— 連的是⟦Azure 內部的兩個虛擬網路⟧，流量走 Microsoft 骨幹直接互通，看起來像同一個網路，低延遲、高頻寬，而且不需要閘道。同區域叫 VNet peering，跨區域叫全域 VNet peering。它與地端無關。
記法：⟦要私人專線進雲 → ExpressRoute；要便宜、加密、走網際網路 → VPN 閘道；要把兩個 Azure 虛擬網路接起來 → 對等互連⟧。

【透過私人連線把地端網路延伸到 Microsoft 雲端】→ ExpressRoute
關鍵字是「私人連線」。不經過公用網際網路的只有 ExpressRoute。

【把兩個以上的 Azure 虛擬網路合併成單一邏輯虛擬網路】→ 虛擬網路對等互連
關鍵字是「Azure 虛擬網路之間」。兩端都在 Azure 內，就是對等互連。

【透過公用網路，提供從地端網路到 Azure 的加密連線】→ VPN 閘道
關鍵字是「公用網路」加「加密」。走公網但要安全，答案就是 VPN。"""

EN387 = """Separate the three connectivity options once:
・⟦ExpressRoute⟧ — a ⟦private connection⟧ into the Microsoft backbone through a connectivity provider, never touching the public internet. Bandwidth from 50 Mbps to 100 Gbps, predictable latency and an SLA; suited to large data transfers, hybrid production environments and latency-sensitive applications. Three models: CloudExchange co-location, point-to-point Ethernet, and any-to-any (IPVPN). The most expensive option.
・⟦VPN gateway⟧ — travels the ⟦public internet⟧ but encrypts the traffic (IPsec/IKE). Site-to-site (S2S: an on-premises VPN device to Azure), point-to-site (P2S: a single client device to Azure) and VNet-to-VNet. Quick and cheap to stand up, but bandwidth and latency follow whatever the internet is doing.
・⟦Virtual network peering⟧ — connects ⟦two virtual networks inside Azure⟧ over the Microsoft backbone, so they behave as one network with low latency, high bandwidth and no gateway required. Within a region it is VNet peering; across regions, global VNet peering. It has nothing to do with on-premises.
Rule of thumb: ⟦private circuit into the cloud → ExpressRoute; cheap encrypted link over the internet → VPN gateway; joining two Azure virtual networks → peering⟧.

[Extends on-premises networks to the Microsoft cloud via a private connection] -> ExpressRoute
The key phrase is 'private connection'. Only ExpressRoute stays off the public internet.

[Combines two or more Azure virtual networks into a single logical virtual network] -> Virtual network peering
The key phrase is 'Azure virtual networks'. Both ends inside Azure means peering.

[Provides an encrypted connection from on-premises networks to Azure via a public network] -> VPN gateway
The key words are 'public network' and 'encrypted'. Over the public internet but secure means VPN."""

patch(L, 387, """Question #387  ·  Topic 1  ·  DRAG DROP
Match the Azure services to the appropriate descriptions.
To answer, drag the appropriate service from the column on the left to its description on the right. Each service may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.

Services：ExpressRoute ｜ Virtual network peering ｜ VPN gateway

Answer Area（紅框標出的正解順序）
1. Extends on-premises networks to the Microsoft cloud via a private connection　→　ExpressRoute
2. Combines two or more Azure virtual networks into a single logical virtual network　→　Virtual network peering
3. Provides an encrypted connection from on-premises networks to Azure via a public network　→　VPN gateway

（核對來源：PDF 第 113 頁）""", line_edits=[
    (" e:", ' e:' + js(E387) + ','),
    ("     tgt:[", '     tgt:' + arr(["⟦Extends on-premises networks to the Microsoft cloud via a private connection⟧",
                                     "⟦Combines two or more Azure virtual networks into a single logical virtual network⟧",
                                     "⟦Provides an encrypted connection from on-premises networks to Azure via a public network⟧"]) + ','),
    ("     e:", '     e:' + js(EN387) + '}},'),
])

# ══ #395（PDF 第 116 頁）═════════════════════════════════════════════
E395 = """儲存體帳戶底下四種服務，一次分清楚（可拖曳欄四個、答案區三格，⟦磁碟儲存體是干擾項⟧）：
・⟦Azure Blob 儲存體⟧— 存放非結構化的物件：圖片、影片、備份、記錄檔、資料湖。有⟦存取層⟧可設：熱（經常存取）、冷（至少 30 天）、冷卻（至少 90 天）、封存（至少 180 天，離線保存，讀取前要先解凍／重新水合，可能要數小時）。三種 Blob 類型：區塊、附加、分頁。
・⟦Azure 檔案儲存體（Azure Files）⟧— 完全受控的檔案共用，走 ⟦SMB⟧ 或 NFS 通訊協定，Windows／Linux／macOS 都能像網路磁碟機一樣掛載，也能用 Azure 檔案同步快取到地端伺服器。
・⟦Azure 佇列儲存體（Queue Storage）⟧— 應用程式元件之間的⟦非同步訊息⟧佇列，用來解耦與削峰：前端把工作丟進佇列，後端慢慢取出處理。單一訊息最大 64 KB，可存放數百萬則。
・⟦Azure 磁碟儲存體（Disk storage）⟧— 給虛擬機器用的區塊層級磁碟（Ultra Disk、進階 SSD、標準 SSD、標準 HDD），一次只掛在一台虛擬機器上，不是共用檔案服務。
注意：⟦Azure Service Bus 也是訊息服務，功能比佇列儲存體更豐富（主題與訂閱、交易、順序保證），但它不屬於儲存體帳戶。本題只在四種儲存體服務裡選，答案就是佇列儲存體⟧。

【用於應用程式之間的可靠訊息傳遞】→ Azure 佇列儲存體
關鍵字是「訊息」。四種儲存體服務裡只有佇列是為訊息設計的。

【可以從 Windows 裝置以網路共用的方式存取】→ Azure 檔案儲存體
關鍵字是「網路共用」。SMB 掛載成磁碟機是 Azure Files 的招牌能力；Blob 要靠 Blobfuse 之類的工具才勉強做得到。

【可以設定成使用封存（Archive）存取層】→ Azure Blob 儲存體
關鍵字是「封存存取層」。存取層是 Blob 專屬的概念，而且封存層只能設在個別 Blob 上，不能設成帳戶預設層。"""

EN395 = """Separate the four services inside a storage account once (four are offered, three boxes are used, so ⟦Disk storage is the distractor⟧):
・⟦Azure Blob storage⟧ — unstructured objects: images, video, backups, logs, data lakes. It has ⟦access tiers⟧: hot (frequent access), cool (at least 30 days), cold (at least 90 days) and archive (at least 180 days, stored offline and needing rehydration — potentially hours — before it can be read). Three blob types: block, append and page.
・⟦Azure Files⟧ — a fully managed file share over ⟦SMB⟧ or NFS, mountable as a network drive from Windows, Linux and macOS, and cacheable on-premises with Azure File Sync.
・⟦Azure Queue Storage⟧ — an ⟦asynchronous message⟧ queue between application components, used to decouple and to absorb spikes: the front end drops work on the queue and the back end takes it off at its own pace. Messages up to 64 KB, millions of them.
・⟦Azure Disk storage⟧ — block-level disks for virtual machines (Ultra Disk, premium SSD, standard SSD, standard HDD), attached to one VM at a time rather than shared as a file service.
Note: ⟦Azure Service Bus is also a messaging service and a richer one (topics and subscriptions, transactions, ordering guarantees), but it does not live in a storage account. This question chooses among the four storage services, so the answer is Queue Storage⟧.

[Used for reliable messaging between applications] -> Azure Queue Storage
The key word is messaging. Of the four storage services, only the queue is built for it.

[Can be accessed as a network share from a Windows device] -> Azure Files
The key phrase is 'network share'. Mounting over SMB as a drive letter is the signature capability of Azure Files; Blob needs something like Blobfuse even to approximate it.

[Can be configured to use the Archive access tier] -> Azure Blob storage
The key phrase is 'Archive access tier'. Access tiers are a Blob concept, and archive in particular can only be set on an individual blob, never as the account default tier."""

patch(L, 395, """Question #395  ·  Topic 1  ·  DRAG DROP
Match the Azure storage services to the appropriate descriptions.
To answer, drag the appropriate storage service from the column on the left to its description on the right. Each service may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.

Storage service：Azure Blob storage ｜ Azure Disk storage ｜ Azure Files ｜ Azure Queue Storage

Answer Area（紅框標出的正解順序）
1. Used for reliable messaging between applications　→　Azure Queue Storage
2. Can be accessed as a network share from a Windows device　→　Azure Files
3. Can be configured to use the Archive access tier　→　Azure Blob storage

（核對來源：PDF 第 116 頁。Azure Disk storage 是沒有用到的干擾項）""", line_edits=[
    (" e:", ' e:' + js(E395) + ','),
    ("     tgt:[", '     tgt:' + arr(["⟦Used for reliable messaging between applications⟧",
                                     "⟦Can be accessed as a network share from a Windows device⟧",
                                     "⟦Can be configured to use the Archive access tier⟧"]) + ','),
    ("     e:", '     e:' + js(EN395) + '}},'),
])

save(L)
print("批次 E 完成：#249 #272 #287 #386 #387 #395")
