# DailyNewsBot
每日自动爬取新闻（主要聚焦于作者感兴趣的网站），存入向量数据库，在main页面中可以进行问答，LLM可以检索相似向量文本进行回答，同时，也会有每日小报推送功能、新闻稿撰写功能等。
目前主要功能待实现
## 环境配置
python=3.10
pip install -r requirements.txt

## 启动方式
因为底模型使用huggingface上的THUDM/chatglm3-6b，或者是openai的api，需要使用海外服务器或者其他方式
之后使用 
streamlit run main.py 
启动