import win32com.client

speaker = win32com.client.Dispatch("SAPI.SpVoice")
voices = speaker.GetVoices()

for i in range(voices.Count):
    v = voices.Item(i)
    print(v.GetDescription())