# -*- coding: utf-8 -*-
"""核對原文 批次 B：#116 #124 #133 #137 #138 #140（PDF 第 35、37、40、41、42 頁）。
   同時把解析改寫成「共用對照一次 + 逐格重點」（SPEC §8-5）。一次性腳本，保留供追溯。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vfy import load, save, patch, js, arr, arr2, _span

L = load()

# ══ #116（PDF 第 35 頁）══════════════════════════════════════════════
# 原文兩個下拉都是 1/2/3，反推版本把第一格改成 2/1/3；改回原文順序並重對 a。
E116 = """99.99% 這個數字只有一種湊法：⟦兩台以上的虛擬機器，分別部署在兩個以上的可用性區域⟧，兩個條件缺一不可。
虛擬機器 SLA 的五個級距（整組記）：
・95%（每月約停 36 小時）— 單一虛擬機器，標準 HDD 磁碟。
・99.5%（約 3.6 小時）— 單一虛擬機器，標準 SSD 磁碟。
・99.9%（約 43 分鐘）— 單一虛擬機器，作業系統與資料磁碟全用進階 SSD 或 Ultra Disk。
・99.95%（約 22 分鐘）— 兩台以上的虛擬機器放在同一個⟦可用性設定組⟧，分散故障網域與更新網域，防的是機架故障與主機更新。
・99.99%（約 4.3 分鐘）— 兩台以上的虛擬機器分散在兩個以上的⟦可用性區域⟧，防的是整個資料中心失效。
再往上就得跨區域，那已經是災難復原的層次，SLA 不會再加。
題目問的是⟦「最少」數量⟧，所以兩格都填剛好滿足條件的 2，不要多填。

【應該建議的虛擬機器最少數量】→ 2
只有一台機器時，不管放在哪個區域，機器重新開機或故障服務就中斷，連 99.95% 都拿不到。

【應該建議的可用性區域最少數量】→ 2
只用一個可用性區域，最高只到 99.95%，而且還得靠可用性設定組；單一資料中心整個失效時服務就沒了。
可用性區域的基本概念：每個支援的 Azure 區域至少有三個可用性區域，各自是實體獨立的資料中心，有獨立的電力、冷卻與網路；彼此距離夠遠不會被同一場災害波及，又夠近（來回延遲通常在 2 毫秒以內）可以做同步複寫。用法分為區域固定（zonal，你指定資源放在哪一個區域）與區域備援（zone-redundant，平台自動跨區域散布，例如 ZRS 儲存體）。開三個區域可用性更好，但不是達成 99.99% 的必要條件。"""

EN116 = """There is only one way to reach 99.99%: ⟦two or more virtual machines deployed across two or more availability zones⟧. Both halves are required.
The virtual machine SLA tiers, as one set:
・95% (about 36 hours of downtime a month) — a single VM on standard HDD disks.
・99.5% (about 3.6 hours) — a single VM on standard SSD disks.
・99.9% (about 43 minutes) — a single VM with premium SSD or Ultra Disk for every OS and data disk.
・99.95% (about 22 minutes) — two or more VMs in one ⟦availability set⟧, spread across fault and update domains, protecting against rack failure and host updates.
・99.99% (about 4.3 minutes) — two or more VMs across two or more ⟦availability zones⟧, protecting against the loss of a whole datacenter.
Beyond that you have to cross regions, which is disaster recovery territory and earns no further SLA.
The question asks for the ⟦minimum⟧, so each box takes the smallest value that satisfies the condition — 2 — and nothing more.

[Minimum number of virtual machines] -> 2
With one machine, in any zone, the service still goes down when it reboots or fails; it cannot even reach 99.95%.

[Minimum number of availability zones] -> 2
A single zone tops out at 99.95%, and only with an availability set, because losing that one datacenter takes the service with it.
Availability zone basics: every supported Azure region has at least three zones, each a physically separate datacenter with independent power, cooling and networking; they are far enough apart that one disaster cannot take out more than one, yet close enough (round-trip latency typically under 2 ms) for synchronous replication. They are used either zonally (you pin a resource to a specific zone) or zone-redundantly (the platform spreads it for you, as with ZRS storage). Three zones give better availability but are not required for 99.99%."""

patch(L, 116, """Question #116  ·  Topic 1  ·  HOTSPOT
You plan to deploy a critical line-of-business application to Azure.
The application will run on an Azure virtual machine.
You need to recommend a deployment solution for the application. The solution must provide a guaranteed availability of 99.99 percent.
What is the minimum number of virtual machines and the minimum number of availability zones you should recommend for the deployment? To answer, select the appropriate options in the answer area.
NOTE: Each correct selection is worth one point.
Hot Area:

Answer Area
Minimum number of virtual machines:　▼　1 ｜ 2 ｜ 3
Minimum number of availability zones:　▼　1 ｜ 2 ｜ 3

紅框標出的正解
1. Minimum number of virtual machines　→　2
2. Minimum number of availability zones　→　2

（核對來源：PDF 第 35 頁）""", line_edits=[
    (" q:", ' q:' + js("你打算把一個關鍵的營運（LOB）應用程式部署到 Azure，它會在一台 Azure 虛擬機器上執行。\n"
                       "你要為這個應用程式建議部署方案，⟦方案必須提供 99.99% 的保證可用性⟧。\n"
                       "這個部署你應該建議的虛擬機器最少數量與可用性區域最少數量各是多少？請在答案區選出正確的選項。") + ','),
    (" sent:", ' sent:' + js("應該建議的虛擬機器最少數量：{0}\n應該建議的可用性區域最少數量：{1}") + ','),
    (" dd:[", ' dd:' + arr2([["1", "2", "3"], ["1", "2", "3"]]) + ','),
    (" a:[", ' a:[1,1],'),
    (" e:", ' e:' + js(E116) + ','),
    (" en:{q:", ' en:{q:' + js("You plan to deploy a critical line-of-business application to Azure.\n"
                               "The application will run on an Azure virtual machine.\n"
                               "You need to recommend a deployment solution for the application. ⟦The solution must provide a guaranteed availability of 99.99 percent⟧.\n"
                               "What is the minimum number of virtual machines and the minimum number of availability zones you should recommend for the deployment? To answer, select the appropriate options in the answer area.") + ','),
    ("     sent:", '     sent:' + js("Minimum number of virtual machines: {0}\nMinimum number of availability zones: {1}") + ','),
    ("     dd:[", '     dd:' + arr2([["1", "2", "3"], ["1", "2", "3"]]) + ','),
    ("     e:", '     e:' + js(EN116) + '}},'),
])

# ══ #124（PDF 第 37 頁）══════════════════════════════════════════════
# 原文的描述是名詞片語「A managed service that…」，反推版本前面多了「是 / is」。
E124 = """Azure 的 IoT 服務由淺到深三層，這一題三格剛好各取一層：
・⟦Azure IoT 中樞（IoT Hub）— 平台即服務（PaaS）的訊息中樞⟧。裝置與雲端之間的雙向通道：裝置到雲端的遙測，以及雲端到裝置的命令、直接方法與裝置對應項（device twin）。支援 MQTT、AMQP、HTTPS，每個裝置有自己的身分與認證（對稱金鑰、X.509 憑證、TPM），可以逐一驗證與撤銷。它只給你通道與裝置管理，儀表板、規則、儲存都要自己接。
・⟦Azure IoT Central — 軟體即服務（SaaS）的完整 IoT 應用平台⟧。底下其實包了一個 IoT 中樞，但把裝置範本、儀表板、規則與警示、使用者管理、資料匯出全部做好，用瀏覽器設定就能上線，不必寫程式也不必管理基礎結構。
・⟦Azure Sphere — 軟硬體整合的安全性解決方案⟧。三個部分：內建 Microsoft Pluton 安全子系統的認證微控制器（MCU）、以 Linux 為基礎的 Azure Sphere OS、以及雲端的 Azure Sphere 安全性服務（憑證式驗證、錯誤回報、自動安全性更新）。它管的是「這台裝置本身可不可信」，層次比前兩個更底層。
判斷訣竅：⟦看到「雙向通訊」選 IoT 中樞、看到「SaaS／大規模連線監視管理」選 IoT Central、看到「軟體加硬體／安全性」選 Azure Sphere⟧。

【提供 IoT 裝置與 Azure 之間雙向通訊的受控服務】→ IoT 中樞（IoT Hub）
關鍵字是「雙向」。單向只收遙測用 Event Hubs 就夠了；要能從雲端回頭下命令、更新裝置設定，才需要 IoT 中樞。

【完全受控的軟體即服務（SaaS）解決方案，用來大規模連線、監視與管理 IoT 裝置】→ IoT Central
關鍵字是「SaaS」。三個服務裡只有 IoT Central 是 SaaS，開箱即用；IoT 中樞是 PaaS，要自己組應用程式。

【為 IoT 裝置提供通訊與安全性功能的軟硬體整合解決方案】→ Azure Sphere
關鍵字是「軟體加硬體」。只有 Azure Sphere 連晶片一起管，另外兩個都是純雲端服務。"""

EN124 = """Azure's IoT services stack up in three layers, and the three boxes take one each:
・⟦Azure IoT Hub — a platform as a service (PaaS) message hub⟧. A two-way channel between devices and the cloud: device-to-cloud telemetry, plus cloud-to-device commands, direct methods and device twins. It speaks MQTT, AMQP and HTTPS, and every device has its own identity and credential (symmetric key, X.509 certificate, TPM) that can be authenticated and revoked individually. It gives you the channel and device management; dashboards, rules and storage are yours to wire up.
・⟦Azure IoT Central — a fully managed software as a service (SaaS) IoT application platform⟧. It wraps an IoT Hub underneath, but device templates, dashboards, rules and alerts, user management and data export are all built for you — configure it in a browser, no code and no infrastructure to manage.
・⟦Azure Sphere — a combined software and hardware security solution⟧. Three parts: a certified microcontroller (MCU) with the Microsoft Pluton security subsystem built in, the Linux-based Azure Sphere OS, and the cloud-side Azure Sphere Security Service (certificate-based authentication, error reporting, automatic security updates). It answers 'can this device itself be trusted', a lower layer than the other two.
Rule of thumb: ⟦'bidirectional communication' → IoT Hub, 'SaaS / connect, monitor and manage at scale' → IoT Central, 'software and hardware / security' → Azure Sphere⟧.

[A managed service that provides bidirectional communication between IoT devices and Azure] -> IoT Hub
The key word is bidirectional. One-way telemetry ingestion would be satisfied by Event Hubs; sending commands and configuration back down to the device is what requires IoT Hub.

[A fully managed software as a service (SaaS) solution to connect, monitor, and manage IoT devices at scale] -> IoT Central
The key word is SaaS. Of the three, only IoT Central is SaaS and usable out of the box; IoT Hub is PaaS and expects you to build the application around it.

[A software and hardware solution that provides communication and security features for IoT devices] -> Azure Sphere
The key phrase is software and hardware. Only Azure Sphere reaches down to the silicon; the other two are pure cloud services."""

patch(L, 124, """Question #124  ·  Topic 1  ·  DRAG DROP
Match the Azure Services service to the correct description.
Instructions: To answer, drag the appropriate service from the column on the left to its description on the right. Each service may be used once, more than once, or not at all.
NOTE: Each correct selection is worth one point.
Select and Place:

Services：Azure Sphere ｜ IoT Central ｜ IoT Hub

Answer Area（紅框標出的正解順序）
1. A managed service that provides bidirectional communication between IoT devices and Azure　→　IoT Hub
2. A fully managed software as a service (SaaS) solution to connect, monitor, and manage IoT devices at scale　→　IoT Central
3. A software and hardware solution that provides communication and security features for IoT devices　→　Azure Sphere

（核對來源：PDF 第 37 頁）""", line_edits=[
    (" tgt:[", ' tgt:' + arr(["⟦提供 IoT 裝置與 Azure 之間雙向通訊的受控服務⟧",
                             "⟦完全受控的軟體即服務（SaaS）解決方案，用來大規模連線、監視與管理 IoT 裝置⟧",
                             "⟦為 IoT 裝置提供通訊與安全性功能的軟硬體整合解決方案⟧"]) + ','),
    (" e:", ' e:' + js(E124) + ','),
    ("     tgt:[", '     tgt:' + arr(["⟦A managed service that provides bidirectional communication between IoT devices and Azure⟧",
                                     "⟦A fully managed software as a service (SaaS) solution to connect, monitor, and manage IoT devices at scale⟧",
                                     "⟦A software and hardware solution that provides communication and security features for IoT devices⟧"]) + ','),
    ("     e:", '     e:' + js(EN124) + '}},'),
])

# ══ #133（PDF 第 40 頁）══════════════════════════════════════════════
# 原文描述是名詞片語，且紅框只圈關鍵字；把「是 / is」拿掉、標記收窄到紅框範圍。
E133 = """三個資料與分析服務的定位一次分清楚：
・⟦Azure Synapse Analytics — 企業級資料倉儲與分析平台⟧（前身是 SQL 資料倉儲）。處理的是已經整理過的結構化資料，用 T-SQL 做大規模分析查詢。提供專用 SQL 集區（預先配置效能單位，適合穩定的重負載）與無伺服器 SQL 集區（依查詢掃描的資料量計費，適合臨時查詢），並整合 Spark 集區、資料整合管線與 Power BI。資料列／資料行層級安全性、動態資料遮罩、透明資料加密都內建，不另外收費。
・⟦Azure Cosmos DB — 全球散發的多模型 NoSQL 資料庫⟧。一鍵把資料複寫到任意數量的 Azure 區域，個位數毫秒延遲；五種一致性層級（強式、限定過期、工作階段、一致前置詞、最終）讓你在一致性與效能之間調；多區域寫入時提供 99.999% 的讀寫 SLA。多種 API：NoSQL（原生）、MongoDB、Cassandra、Gremlin（圖形）、Table。
・⟦Azure HDInsight — 雲端上的受控開放原始碼大數據叢集⟧。直接開好 Hadoop、Spark、Hive、Kafka、HBase 這些叢集，適合處理尚未整理的原始巨量資料，批次與串流都可以。
記法：⟦「資料倉儲」→ Synapse、「全球散發 + NoSQL」→ Cosmos DB、「Hadoop 叢集」→ HDInsight⟧。

【完全受控的資料倉儲，在各種規模下都內建安全性且不另外收費】→ Azure Synapse Analytics
關鍵字是「資料倉儲」。資料倉儲存的是整理過、可直接分析的結構化資料，與 HDInsight 那種未整理的原始資料湖不同。

【全球散發的支援 NoSQL 的資料庫】→ Azure Cosmos DB
關鍵字是「全球散發」加「NoSQL」。這兩個字同時出現時只有 Cosmos DB；Azure SQL Database 是關聯式，也不是為多區域寫入設計的。

【雲端上的受控 Apache Hadoop 叢集，讓你能處理巨量資料】→ Azure HDInsight
關鍵字是「Apache Hadoop」。題目直接點名開放原始碼的叢集框架，那就是 HDInsight。"""

EN133 = """Place the three data and analytics services side by side once:
・⟦Azure Synapse Analytics — the enterprise data warehouse and analytics platform⟧ (formerly SQL Data Warehouse). It works on structured data that has already been curated, queried at scale with T-SQL. Dedicated SQL pools reserve performance units for steady heavy workloads; serverless SQL pools bill by the data each query scans, which suits ad-hoc work. Spark pools, data integration pipelines and Power BI are integrated. Row- and column-level security, dynamic data masking and transparent data encryption are built in at no extra cost.
・⟦Azure Cosmos DB — the globally distributed multi-model NoSQL database⟧. Replicate to any number of Azure regions with a click, at single-digit millisecond latency; five consistency levels (strong, bounded staleness, session, consistent prefix, eventual) let you trade consistency against performance; multi-region writes come with a 99.999% read and write SLA. Multiple APIs: NoSQL (native), MongoDB, Cassandra, Gremlin (graph) and Table.
・⟦Azure HDInsight — managed open-source big data clusters in the cloud⟧. Hadoop, Spark, Hive, Kafka and HBase clusters stood up for you, suited to raw, uncurated data at massive volume, batch or streaming.
Rule of thumb: ⟦'data warehouse' → Synapse, 'globally distributed + NoSQL' → Cosmos DB, 'Hadoop clusters' → HDInsight⟧.

[A fully managed data warehouse that has integral security at every level of scale at no extra cost] -> Azure Synapse Analytics
The key phrase is data warehouse — curated, analysis-ready structured data, as opposed to the raw data lake that HDInsight chews through.

[A globally distributed database that supports NoSQL] -> Azure Cosmos DB
The key phrases are globally distributed and NoSQL. Together they can only be Cosmos DB; Azure SQL Database is relational and is not built for multi-region writes.

[Managed Apache Hadoop clusters in the cloud that enable you to process massive amounts of data] -> Azure HDInsight
The key phrase is Apache Hadoop. The question names the open-source cluster framework outright, and that is HDInsight."""

patch(L, 133, """Question #133  ·  Topic 1  ·  DRAG DROP
Match the Azure service to the appropriate description.
To answer, drag the appropriate service from the column on the left to its description on the right. Each service may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.
Select and Place:

Services：Azure Cosmos DB ｜ Azure HDInsight ｜ Azure Synapse Analytics

Answer Area（紅框標出的正解順序；描述裡的 [ ] 是紅框另外圈起來的關鍵字）
1. A fully managed [data warehouse] that has integral security at every level of scale at no extra cost.　→　Azure Synapse Analytics
2. A globally distributed [database that supports NoSQL.]　→　Azure Cosmos DB
3. Managed Apache Hadoop clusters in the cloud that enable you to [process massive amounts of data.]　→　Azure HDInsight

（核對來源：PDF 第 40 頁）""", line_edits=[
    (" tgt:[", ' tgt:' + arr(["完全受控的⟦資料倉儲⟧，在各種規模下都內建安全性且不另外收費",
                             "全球散發的⟦支援 NoSQL 的資料庫⟧",
                             "雲端上的受控 Apache Hadoop 叢集，讓你能⟦處理巨量資料⟧"]) + ','),
    (" e:", ' e:' + js(E133) + ','),
    ("     tgt:[", '     tgt:' + arr(["A fully managed ⟦data warehouse⟧ that has integral security at every level of scale at no extra cost",
                                     "A globally distributed ⟦database that supports NoSQL⟧",
                                     "Managed Apache Hadoop clusters in the cloud that enable you to ⟦process massive amounts of data⟧"]) + ','),
    ("     e:", '     e:' + js(EN133) + '}},'),
])

# ══ #137（PDF 第 41 頁）══════════════════════════════════════════════
E137 = """整題只有兩個服務，三格都在同一條分界線上，先把它們一次分清楚：
・⟦Azure Functions — 程式碼優先的無伺服器運算⟧。你寫一段函式（C#、JavaScript、Python、Java、PowerShell…），設定觸發程序（HTTP 要求、計時器、佇列訊息、Blob 建立、Cosmos DB 變更摘要…），平台在事件發生時執行它，依執行次數與「執行時間 × 記憶體」計費。想做什麼邏輯都可以，因為那就是你自己的程式碼。⟦預設無狀態⟧，每次執行彼此獨立，要保存狀態得改用 Durable Functions（協調器函式與實體函式）。可以用 Core Tools 在本機開發與偵錯，也能打包成容器跑在 Kubernetes、Container Apps 甚至地端。
・⟦Azure Logic Apps — 設計工具優先的無伺服器整合⟧。你在視覺化畫布上拉出工作流程，串接數百個現成連接器（Office 365、Salesforce、SQL、Twitter、SAP…），幾乎不必寫程式，依動作執行次數計費。⟦工作流程天生保存每一步的狀態與輸入輸出⟧，執行歷程可以逐步檢視與重播。消費型方案只在 Azure 雲端執行，沒有可下載到本機的執行階段（較新的「標準」方案基於 Functions 執行階段，確實可以本機開發與容器化，但這題比較的是傳統認知下的兩個服務）。
選用原則：⟦要自訂運算邏輯、演算法、資料轉換 → Functions；要串接一堆現成 SaaS 服務、做審核或通知流程 → Logic Apps⟧。兩者可以互相呼叫，實務上常混用：Logic Apps 負責編排流程，中間某一步呼叫 Function 做複雜運算。

【執行程式碼】→ Azure Functions
「程式碼」三個字就是分界：Functions 跑的是你自己寫的函式，Logic Apps 跑的是設計工具拉出來的流程。

【永遠具狀態（is always stateful）】→ Azure Functions
原始文件圈的是 Azure Functions。注意：⟦這個標記在社群有爭議，多數資料認為應該是 Azure Logic Apps⟧ — Logic Apps 的工作流程本來就保存狀態，Functions 預設無狀態、要 Durable Functions 才具狀態。忠實照原始文件作答，但要記住這個更正。

【只能在雲端執行】→ Azure Logic Apps
反過來用「能不能離開雲端」分：Functions 可以在本機與容器裡跑，Logic Apps 的消費型方案只能待在 Azure 上。"""

EN137 = """Only two services are in play and all three boxes turn on the same dividing line, so lay them out once:
・⟦Azure Functions — code-first serverless compute⟧. You write a function (C#, JavaScript, Python, Java, PowerShell and more), configure a trigger (HTTP request, timer, queue message, blob creation, Cosmos DB change feed), and the platform runs it when the event fires, billing by execution count and duration × memory. Any logic is possible because it is your own code. It is ⟦stateless by default⟧ — each execution is independent — and statefulness requires the Durable Functions extension with its orchestrator and entity functions. Core Tools let you develop and debug locally, and the runtime packages into a container for Kubernetes, Container Apps or even on-premises.
・⟦Azure Logic Apps — designer-first serverless integration⟧. You build a workflow on a visual canvas, wiring hundreds of ready-made connectors (Office 365, Salesforce, SQL, Twitter, SAP) together with little or no code, billed per action execution. A workflow ⟦inherently persists the state, inputs and outputs of every step⟧, and run history can be inspected step by step and replayed. The Consumption plan runs only in the Azure cloud, with no runtime to download (the newer Standard plan sits on the Functions runtime and can be developed locally and containerised, but this question compares the two services as traditionally understood).
Choosing between them: ⟦custom computation, algorithms or data transformation → Functions; wiring up many existing SaaS services, approval or notification flows → Logic Apps⟧. They call each other freely, and mixing them is common: Logic Apps orchestrates, and one step calls a Function for the heavy work.

[Executes code] -> Azure Functions
The word 'code' is the dividing line: Functions runs the function you wrote, Logic Apps runs the flow you drew.

[Is always stateful] -> Azure Functions
The source document boxes Azure Functions. Note: ⟦this marking is disputed, and most references give Azure Logic Apps⟧ — a Logic Apps workflow persists state by nature, while Functions is stateless by default and only stateful via Durable Functions. Answer as the source has it, but remember the correction.

[Runs only in the cloud] -> Azure Logic Apps
Turn the line around and ask what can leave the cloud: Functions runs locally and in containers, while the Logic Apps Consumption plan stays on Azure."""

patch(L, 137, """Question #137  ·  Topic 1  ·  DRAG DROP
Match the serverless solution to the correct characteristic.
To answer, drag the appropriate serverless solution from the column on the left to its characteristic on the right. Each serverless solution may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.
Select and Place:

Serverless Solutions：Azure Functions ｜ Azure Logic Apps

Answer Area（紅框標出的正解順序）
1. Executes code:　→　Azure Functions
2. Is always stateful:　→　Azure Functions
3. Runs only in the cloud:　→　Azure Logic Apps

（核對來源：PDF 第 41 頁。第 2 格的標記有爭議，見解析）""", line_edits=[
    (" e:", ' e:' + js(E137) + ','),
    ("     e:", '     e:' + js(EN137) + '}},'),
])

# ══ #138（PDF 第 42 頁）══════════════════════════════════════════════
# 原文描述以動詞開頭「Restrict…」，反推版本前面多了「可以 / can」。
E138 = """原文的可拖曳欄有四個治理功能，答案區只有三格，⟦Azure 資源鎖定是沒有用到的干擾項⟧。四個一起記：
・⟦Azure 原則（Azure Policy）— 管「能不能建、能建成什麼樣」⟧。用 JSON 原則定義搭配效果：Deny（直接擋下）、Audit（放行但記錄不合規）、Append／Modify（自動補上設定或標籤）、DeployIfNotExists（自動部署缺少的元件）。指派到管理群組、訂用帳戶或資源群組，範圍往下繼承。典型用途：只允許特定虛擬機器大小、只允許特定區域、強制加標籤、強制開啟加密。
・⟦Azure 標籤（tags）— 名稱／值配對的中繼資料⟧，貼在訂用帳戶、資源群組或個別資源上。本身不改變任何行為，價值在成本歸屬與資源整理：成本分析可以依標籤分組，算出各成本中心、各專案、各環境花了多少。標籤不會自動從資源群組繼承到底下的資源，要靠 Azure 原則補。
・⟦Azure 藍圖（Azure Blueprints）— 打包一整套環境⟧。把 ARM 範本（資源）、原則指派、角色指派、資源群組四類成品收進一個可版本控管的定義，一次指派就把符合規範的環境整套建起來，還能用藍圖鎖定防止事後被改。
・⟦Azure 資源鎖定（resource locks）— 防呆⟧。CanNotDelete（可讀可改不可刪）與 ReadOnly（只能讀）兩種，蓋過 RBAC 權限，避免正式環境被誤刪誤改。
一句話分：⟦Policy 管規則、tags 管標籤與成本歸屬、Blueprints 管整套環境的部署、locks 管不要被誤刪⟧。

【限制訂用帳戶中能建立哪些類型的虛擬機器】→ Azure 原則（Azure Policy）
關鍵字是「限制…能建立」。只有 Azure 原則能在建立當下擋下不合規的資源；RBAC 管的是「誰可以做」，不是「可以做成什麼樣」。

【找出與特定成本中心相關聯的 Azure 資源】→ Azure 標籤（Azure tags）
關鍵字是「成本中心」。成本歸屬靠標籤，這是標籤最主要的用途。

【部署一整套完整的 Azure 應用程式環境，包含資源設定與角色指派】→ Azure 藍圖（Azure Blueprints）
關鍵字是「一整套」加「角色指派」。ARM 範本只部署資源，把原則與角色指派一起打包的是藍圖。"""

EN138 = """The source lists four governance features but the answer area has only three boxes — ⟦Azure resource locks is the unused distractor⟧. Learn all four together:
・⟦Azure Policy — governs what may be created and how⟧. A JSON policy definition plus an effect: Deny (block outright), Audit (allow but flag as non-compliant), Append/Modify (add settings or tags automatically), DeployIfNotExists (deploy the missing component). Assigned at management group, subscription or resource group, and inherited downward. Typical uses: allow only certain VM sizes, allow only certain regions, require tags, require encryption.
・⟦Azure tags — name/value metadata⟧ attached to subscriptions, resource groups or individual resources. They change no behaviour by themselves; their value is cost attribution and organisation, because Cost Analysis can group by tag to show what each cost centre, project or environment spent. Tags do not inherit from a resource group to the resources inside it — Azure Policy is what fills that gap.
・⟦Azure Blueprints — packages a whole environment⟧. ARM templates (resources), policy assignments, role assignments and resource groups collected into one versioned definition; a single assignment stands up a compliant environment, and blueprint locks stop it being altered afterwards.
・⟦Azure resource locks — the guardrail⟧. CanNotDelete (read and modify but not delete) and ReadOnly (read only), overriding RBAC permissions so production is not deleted or changed by accident.
One line apiece: ⟦Policy is rules, tags are labels and cost attribution, Blueprints is whole-environment deployment, locks are don't-delete-this⟧.

[Restrict which virtual machine types can be created in a subscription] -> Azure Policy
The key phrase is 'restrict which … can be created'. Only Azure Policy blocks a non-compliant resource at creation time; RBAC governs who may act, not what the result may look like.

[Identify Azure resources that are associated with specific cost centers] -> Azure tags
The key phrase is 'cost centers'. Cost attribution runs on tags, and that is what tags are chiefly for.

[Deploy a complete Azure application environment including resources configuration and role assignments] -> Azure Blueprints
The key phrases are 'complete' and 'role assignments'. An ARM template deploys resources only; bundling policy and role assignments alongside them is what Blueprints does."""

patch(L, 138, """Question #138  ·  Topic 1  ·  DRAG DROP
Match the Azure governance feature to the correct description.
Instructions: To answer, drag the appropriate feature from the column on the left to its description on the right. Each feature may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.
Select and Place:

Features：Azure Blueprints ｜ Azure Policy ｜ Azure resource locks ｜ Azure tags

Answer Area（紅框標出的正解順序）
1. Restrict which virtual machine types can be created in a subscription.　→　Azure Policy
2. Identify Azure resources that are associated with specific cost centers.　→　Azure tags
3. Deploy a complete Azure application environment including resources configuration and role assignments.　→　Azure Blueprints

（核對來源：PDF 第 42 頁。Azure resource locks 是沒有用到的干擾項）""", line_edits=[
    (" tgt:[", ' tgt:' + arr(["⟦限制訂用帳戶中能建立哪些類型的虛擬機器⟧",
                             "⟦找出與特定成本中心相關聯的 Azure 資源⟧",
                             "⟦部署一整套完整的 Azure 應用程式環境，包含資源設定與角色指派⟧"]) + ','),
    (" e:", ' e:' + js(E138) + ','),
    ("     tgt:[", '     tgt:' + arr(["⟦Restrict which virtual machine types can be created in a subscription⟧",
                                     "⟦Identify Azure resources that are associated with specific cost centers⟧",
                                     "⟦Deploy a complete Azure application environment including resources configuration and role assignments⟧"]) + ','),
    ("     e:", '     e:' + js(EN138) + '}},'),
])

# ══ #140（PDF 第 42 頁）══════════════════════════════════════════════
# #140 與 #192 是同一題（原始文件重複收錄），描述逐字相同，
# 解析直接沿用 #192 已重寫好的版本，末尾補一句重複收錄的說明。
s, e = _span(L, 192)
E192_LIT = next(x for x in L[s:e] if x.startswith(" e:")).strip()[2:].rstrip(",")
EN192_LIT = next(x for x in L[s:e] if x.startswith("     e:")).strip()[2:].rstrip("}},")

NOTE140 = "\n\n（本題與 #192 是同一題，原始文件重複收錄，兩題都保留。）"
NOTE140_EN = "\n\n(This question and #192 are the same item, recorded twice in the source document; both are kept.)"

patch(L, 140, """Question #140  ·  Topic 1  ·  DRAG DROP
Match the Azure services to the correct descriptions.
Instructions: To answer, drag the appropriate Azure service from the column on the left to its description on the right. Each service may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.
Select and Place:

Services：Azure Functions ｜ Azure App Service ｜ Azure virtual machines ｜ Azure Container Instances

Answer Area（紅框標出的正解順序；描述裡的 [ ] 是紅框另外圈起來的關鍵字）
1. Provide [operating system] virtualization.　→　Azure virtual machines
2. Provide [portable] environment for virtualized applications.　→　Azure Container Instances
3. Used to [build, deploy, and scale web apps.]　→　Azure App Service
4. Provide a platform for [serverless code]　→　Azure Functions

（核對來源：PDF 第 42 頁。本題與 #192 是同一題，原始文件重複收錄）""", line_edits=[
    (" tgt:[", ' tgt:' + arr(["提供⟦作業系統⟧的虛擬化",
                             "為虛擬化的應用程式提供⟦可攜⟧（portable）的執行環境",
                             "是用來⟦建置、部署與擴縮網頁應用程式⟧的",
                             "提供執行⟦無伺服器程式碼⟧（serverless code）的平台"]) + ','),
    (" e:", ' e:' + E192_LIT[:-1] + js(NOTE140)[1:] + ','),
    ("     tgt:[", '     tgt:' + arr(["provides ⟦operating system⟧ virtualization",
                                     "provides a ⟦portable⟧ environment for virtualized applications",
                                     "is used to ⟦build, deploy, and scale web apps⟧",
                                     "provides a platform for ⟦serverless code⟧"]) + ','),
    ("     e:", '     e:' + EN192_LIT[:-1] + js(NOTE140_EN)[1:] + '}},'),
])

# #192 的原文對照補一句：與 #140 是同一題
patch(L, 192, None, text_subs=[
    ("（核對來源：PDF 第 57 頁）", "（核對來源：PDF 第 57 頁。本題與 #140 是同一題，原始文件重複收錄）"),
])

save(L)
print("批次 B 完成：#116 #124 #133 #137 #138 #140（並在 #192 補註重複收錄）")
