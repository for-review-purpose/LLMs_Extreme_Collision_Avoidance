from openai import OpenAI
import time
OPENAI_API_KEY = "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"

client = OpenAI(api_key=OPENAI_API_KEY)

# response = client.files.create(
#   file=open("data_fine_shiyue_exported.jsonl", "rb"),
#   purpose="fine-tune"
# )
#
# time.sleep(5)
#
# file_id = response.id  # 获取文件 ID
#
# # 输出当前的文件列表
# print(client.files.list())
#
# job = client.fine_tuning.jobs.create(
#     training_file=file_id,
#     model="gpt-4o-2024-08-06",
#     method={
#         "type": "supervised",
#     },
# )
#
# # client.fine_tuning.jobs.create(
# #   training_file="file-abc123",
# #   model="gpt-4o-mini"
# # )
#
# #
# # List 10 fine-tuning jobs
# # time.sleep(10)
# print(client.fine_tuning.jobs.list(limit=10))
# #
# #
# time.sleep(10)
# # # Retrieve the state of a fine-tune
print(client.fine_tuning.jobs.retrieve("ftjob-UDweR2xT7Tpp3zn85pFdkjpD"))
