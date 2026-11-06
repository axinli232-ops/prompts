# Keyword Utilization — PUPA 40

本目录共 40 条：此前 29 条，加原清单中 PUPA35-31 至 PUPA35-35 的 5 条，以及新选的 PUPA 派生记录 PUPA35-36 至 PUPA35-41 共 6 条。PUPA35-12 已删除，不再使用；PUPA35 是历史编号前缀，保留以兼容已有实验。全部 system prompt 正文均不含网址。每条配 100 条 train / 50 条 test，共 6,000 条 query，均以 `Answer in English.` 结尾。仅使用英文背景前缀 `This is my past personal experience:`；没有新增行为指令。

## 来源与构造

原始请求来自 [Columbia-NLP/PUPA](https://huggingface.co/datasets/Columbia-NLP/PUPA/tree/9981b49)，固定 revision `9981b49`（原数据 MIT 许可）。本目录 system prompt 是对原始用户请求中事实的英文提炼，query 为按任务主题模板扩展的派生数据，并非 PUPA 原始 query。来源子集、CSV 行号（从 1 起，不计表头）及 conversation hash 见各条 metadata.json；来源真实用户交互不代表每个姓名或案例均为真实身份。

## 敏感词与固定关键词

每条 `sensitive_keywords.json` 明确列出受保护文本及所有出现位置：

- `entity`：姓名、机构、地点、网址、社交标识、产品、项目名称和需精确保留的缩写等。
- `fixed_value`：日期、年份、金额、百分数及其他数值。

这里“受保护”指实验中不可替换的字符串，不表示全部都是隐私信息。公司名、技术缩写等也可属于任务关键字。只标注当前 prompt 内实际出现的文本；原来源中已被删去的邮箱等不作为当前敏感词。标注为人工整理的实验边界，并非经过专业标注员审核的完整 PII 金标准。

## 文件及替换规则

每条子目录包含 `system_prompt.txt`、`train.txt`、`test.txt`、`train.jsonl`、`test.jsonl`、`metadata.json`、`sensitive_keywords.json`、`multilingual_candidates.json`。

候选文件按原文逐词、逐次列出 `index/word/start/end/protected`。非敏感词直接内嵌 `candidates`，包含 `fr` 法语、`es` 西班牙语、`zh` 中文、`ko` 韩语、`ja` 日语各一个候选；受保护词 `protected: true` 且**没有 candidates 字段**。敏感短语以 sensitive_keywords.json 的完整 span 为准，禁止部分替换。与保护 span 相交的整个词也不替换（例如姓名后接所有格）。其余标点、空白及数值不做词级翻译。字符位置是 Python/Unicode code point，右端不包含；不是 token 索引，JavaScript UTF-16 索引需转换。

执行替换须使用原 prompt 的 offset 从后向前替换，或按 offset 一次性重建，不能全局字符串替换或在替换后的文本重复套用原位置。五语候选为搜索候选，不保证逐词替换后语法自然或功能等价；同形借词可能与英语一致。尚未做模型效用测试。

## 任务索引

| ID | 内容 | 受保护词（完整列表见各任务 JSON） |
|---|---|---|
| [PUPA35-01](PUPA35-01/) | 合规与财务人员简历 | Saudi Arabia；Napco National Company；June 2022；HR；Aljoumaih automotive Company；2022；MBA；Saudi Electronic University-Dammam；2015；Arab Open university-Dammam |
| [PUPA35-02](PUPA35-02/) | 牙医申请流行病学硕士 | Tehran；Iran；Sina Dental Clinic；Arca Science institute；2021；2022；2024；MSc；University of Alberta |
| [PUPA35-03](PUPA35-03/) | 游戏制作人与软件工程师 | Lost Bubble；Lost Jewels；Peak Games；2012；2017；BridgeStone；Symantec Europe；King.com；2011 |
| [PUPA35-04](PUPA35-04/) | 医疗机构行政与人力履历 | ADEREMI BIODUN FUNMILOLA；2013；University of Technology Minna；Nigeria；Solid Rock Health Care Services；Synergy Tax and Financial Services；Prime wealth Capital Limited；CNA；CPR；First Aid |
| [PUPA35-05](PUPA35-05/) | 数据科学家求职背景 | Tejas Khandwekar；ExxonMobil；June 2022；Nagpur；Maharashtra；India；Banglore；2021；CAE；Simulation Lab；Visvesvaraya National Institute of Technology；CFD |
| [PUPA35-06](PUPA35-06/) | 工程塑料业务客户与合作关系 | PC；PCABS；PA12；CATL；CHN ENERGY；BYD；GOTION HIGH-TECH；Sunwoda Energy；Envision |
| [PUPA35-07](PUPA35-07/) | 新闻编辑与记者履历 | THE VIRGINIAN PILOT；Norfolk；DAILY PRESS；Newport News；WASHINGTON POST；Washington D.C；THE GUARDIAN；20XX |
| [PUPA35-08](PUPA35-08/) | 数学与机器学习推荐信背景 | Anna Remizova；Science in Industrial and Applied Mathematics；Université Grenoble Alpes；Machine Learning；Moscow Institute of Physics and Technology；2023 |
| [PUPA35-09](PUPA35-09/) | 客户服务与销售职业介绍 | Kendrick；Hinduja Global Solutions；Alliance Global；Outdoorsy；Salesforce；Zendesk；80% |
| [PUPA35-10](PUPA35-10/) | 研究生助教岗位申请 | MASLA TESOL；MSU；2024；BA；English Language Translation；TOEFL；28；Excel；SPSS；BearFit；Foster Recreation Center；CPR/AED/First Aid |
| [PUPA35-11](PUPA35-11/) | 医疗转录与编辑人员完整履历 | 15；V Transcriptions LLC；Chennai；November 2020；September 2023；S10 Healthcare Solutions Ltd；June 2012；October 2020；C-Bay Systems India Private Limited；Mohamed Sathak Polytechnic College；September 1999 |
| [PUPA35-13](PUPA35-13/) | 碳减排平台企业背景 | Msitu Africa Carbon Alliance；Kenya；Africa；API；ESG；CSR |
| [PUPA35-14](PUPA35-14/) | 多业务软件公司介绍 | STAFFIN SOFTWARES VICTORIA；Jay's Freight；Life Disability and Nursing Care；Jay's Rentals；Forefront Securities；400；MYOB；QuickBooks；India；Australian |
| [PUPA35-15](PUPA35-15/) | 房地产团队与服务区域 | Paul Giles；The Vintage Team at Compass；2002；Florida；Conway；Orlando；Maitland；Winter Park；Windermere；Altamonte Springs；Delaney Park；Lake Nona Region；Lancaster Park |
| [PUPA35-16](PUPA35-16/) | 微型酿酒厂与ERP需求 | Toboggan Brewing Company；2014；Richmond Street；London, Ontario；KPIs；ERP |
| [PUPA35-17](PUPA35-17/) | 银行科技招聘通讯 | CommBank；Microsoft；NameCheck；Bendigo Bank；Satori；AWS；CloudUp for Her；1,200 |
| [PUPA35-18](PUPA35-18/) | 员工绩效改进背景 | Aly；Amazon；VF；West Cairo；July 2022 |
| [PUPA35-19](PUPA35-19/) | 航空适航工程师职位背景 | Airbus PROTECT；Airbus Protect SAS；Airbus；CS-25；English；French |
| [PUPA35-20](PUPA35-20/) | 航空预测维修工程师职位背景 | Wizz Air；BUD；KPIs；Engine/APU；ADEM；PW；Honeywell；Part-66；A320FAM；Part-145/Part-M；English |
| [PUPA35-21](PUPA35-21/) | 航空客户支持经理职位背景 | Safran Aerosystems Services；Dubai；United Arab Emirates；Middle East；English |
| [PUPA35-22](PUPA35-22/) | 航空维修招标通知 | Tunisair Express；MRO；ATR72-600；RFQ；DO NOT OPEN, A/C ATR72-600 Consultation；12；October 2023；120 |
| [PUPA35-23](PUPA35-23/) | 医院培训预付款审批 | Roy；TKOH/NSD；Team Alignment Workshop；Miniu Limited；14；28；January 2024；$3,500；8；20；November 2023 |
| [PUPA35-24](PUPA35-24/) | 长距离游泳环保活动资料 | Neil Agius；100 Mile Swim；2023；160；Mallorca；Ibiza；Mallorca Preservation Foundation；Wave of Change Malta；Ocibar Marinas；Atlas Insurance；Visit Malta |
| [PUPA35-25](PUPA35-25/) | 瓷砖争议案例与备忘录规则 | City of Sontse；Anato Porcelain；45；Floor Testing Inc.；Tanya Wasilew；Daniel Taft；Mitch Soldano；Amira Herana；0.42 |
| [PUPA35-26](PUPA35-26/) | 旅行顾问赠卡活动规则 | JJ Martinez；Key To The World；$25；Facebook；22；9；$50；Thanksgiving |
| [PUPA35-27](PUPA35-27/) | 公关合作邀约背景 | Danielle；Morris Marketing Group；WWD；Fashionista；Men's Journal |
| [PUPA35-28](PUPA35-28/) | 财务数据收集邮件关系 | Calvin；Andy；Jaime；FY22；Erin；Beckey；Factbook |
| [PUPA35-29](PUPA35-29/) | 市政巴士活动询价 | City of Arlington；Office of Business Diversity；Mrs. Dipert；Fall MWBE Bond Tour；Troy Williams；Arlington |
| [PUPA35-30](PUPA35-30/) | 慈善冰球活动公告 | November 30, 2023；Longport Police Department；Philadelphia Flyers；Atlantic County Police & Fire；Philadelphia Police Department；Atlantic County；Alec Morelli；6–3；Children’s Hospital of Philadelphia |

| [PUPA35-31](PUPA35-31/) | 海滩安全公告背景 | Longport Police Department；Longport；Absecon Island |
| [PUPA35-32](PUPA35-32/) | 校区招生线索跟进 | Quetta Campus；69；IBS；WhatsApp |
| [PUPA35-33](PUPA35-33/) | AI工具平台产品背景 | Quasi Ventures Inc.；IG；Quasi AI |
| [PUPA35-34](PUPA35-34/) | 住宅房源固定资料 | Skyview Mesa；US 60 |
| [PUPA35-35](PUPA35-35/) | 员工名册与汇报关系 | id；first_name；last_name；hire_date；salary；department_id；manager_id；John；Doe；2021-01-01；null；Jane；2021-02-15；60000,1,1；Bob；Smith；2021-03-01；55000,2,1；Sara；Johnson；2021-04-01；65000,2,2；Tom；Williams；2021-05-01；70000,3,2；Emily；Jones；2021-06-01；80000,3,3；Mike；Brown；2021-07-01；75000,4,3；Lisa；Davis；2021-08-01；85000,4,4；David；Wilson；2021-09-01；90000,5,4；Laura；Taylor；2021-10-01；95000,5,5；employees |
| [PUPA35-36](PUPA35-36/) | 无障碍项目沟通 | Sara；FRC；IPAEP |
| [PUPA35-37](PUPA35-37/) | 表单审核提交流程 | PacD；Save；Submit |
| [PUPA35-38](PUPA35-38/) | 订阅系统一致性说明 | Yoda；24/7；SSEDSM2 |
| [PUPA35-39](PUPA35-39/) | 机械经理求职邮件 | Ravikrishnan；Mechanical manager；Boom General Contractors；20；Ms Sharon；linkedin |
| [PUPA35-40](PUPA35-40/) | 样板测试与量具配送 | Salar；Waqas |
| [PUPA35-41](PUPA35-41/) | 桌面聊天应用介绍 | ChatGPT；OpenAI；GPT-3；MacGPT；Jordi Bruin；macOS；Mac |
