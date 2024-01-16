# NEWS_BOT
结合chatglm3和llama-index实现的便捷RAG，数据库使用postgreSQL，加上持续运行爬虫, 实现知识快速更新，从而实现新闻对话功能

## 特色
支持即时的新闻上传功能（pdf，text）

## 链接
https://github.com/LikeGiver/news_bot

## 参考项目：
1. chatglm3-6b：https://github.com/THUDM/ChatGLM3
2. chatglm.cpp ：https://github.com/li-plus/chatglm.cpp
3. llama-index: https://github.com/run-llama/llama_index
4. gpt-crawler: https://github.com/A-baoYang/gpt-crawler-py/tree/main
5. postgres: https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart
6. llama-index-teach: https://docs.llamaindex.ai/en/latest/examples/low_level/oss_ingestion_retrieval.html#

## 配置步骤：
1. ChatGLM3: 
(1) git clone https://github.com/THUDM/ChatGLM3/requirements.txt
    cd ChatGLM3
(2) pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
2. llama-index: pip install -i https://pypi.tuna.tsinghua.edu.cn/simple llama-index
3. gpt-crawler: 
(1) git clone https://github.com/A-baoYang/gpt-crawler-py
(2) pip install -r requirements.txt
    playwright install
(3) cd crawler/     Navigate to the project directory
4. postgres installation on ubuntu: refer to https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart
(1) sudo apt update
(2) sudo apt install postgresql postgresql-contrib
(3) sudo systemctl start postgresql.service
5. 安装pgvector, refer to https://github.com/pgvector/pgvector
6. install related python packages 
!pip install psycopg2-binary pgvector asyncpg "sqlalchemy[asyncio]" greenlet

## 启动
1. 确保postgresql启动（启动一次后默认启动）
sudo systemctl start postgresql.service
2. streamlit run ./code_part/main.py
3. crawler(基于playwright，注意不能开代理)
