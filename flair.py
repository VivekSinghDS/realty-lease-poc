import requests

url = "https://content-docs.googleapis.com/v1/documents/17yWZSPn_wB09cb2Ln55tnF2zBn8VJBaQSCLajGi0Gqs?includeTabsContent=true"

headers = {
    "accept": "*/*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "authorization": "Bearer ya29.a0AQQ_BDSC8ZphUhM_5XD5R2NM4XCASmFUI11USIPpzvQj1KrRPPKqs3cLnE3sPod3zgVJjRm3SufglPrgOyxqbgvCzfcxGvB361jWqOYN8LaWI-ltsjQ-g_9_IG_qzUxsrX1rbil0Oxz2KvNcoU1L--6rUxWtm91qG8ZYaZbaBvbb1eBdPQcT50w47Cj_jTquXXEAaakaCgYKASUSARcSFQHGX2MiUD9DVLgPv5qu3DxByUMp7A0206",
    "priority": "u=1, i",
    "referer": "https://content-docs.googleapis.com/static/proxy.html?usegapi=1&jsh=m%3B%2F_%2Fscs%2Fabc-static%2F_%2Fjs%2Fk%3Dgapi.lb.en.J8aLcn7bYF8.O%2Fd%3D1%2Frs%3DAHpOoo-YaQN_2soL6ZNher0ZcTp3d4Q_nw%2Fm%3D__features__",
    "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-fetch-storage-access": "active",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "x-browser-channel": "stable",
    "x-browser-copyright": "Copyright 2025 Google LLC. All rights reserved.",
    "x-browser-validation": "jFliu1AvGMEE7cpr93SSytkZ8D4=",
    "x-browser-year": "2025",
    "x-client-data": "CIi2yQEIo7bJAQipncoBCMmFywEIkqHLAQibpMsBCIagzQEI/aXOAQjmhM8BCI+HzwEI+ofPAQjTiM8BCJeMzwEIjY7PAQjtjs8BGLKGzwEYmIjPAQ==",
    "x-clientdetails": "appVersion=5.0%20(Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F140.0.0.0%20Safari%2F537.36&platform=MacIntel&userAgent=Mozilla%2F5.0%20(Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F140.0.0.0%20Safari%2F537.36",
    "x-goog-encode-response-if-executable": "base64",
    "x-javascript-user-agent": "apix/3.0.0 google-api-javascript-client/1.1.0",
    "x-origin": "https://explorer.apis.google.com",
    "x-referer": "https://explorer.apis.google.com",
    "x-requested-with": "XMLHttpRequest"
}

response = requests.get(url, headers=headers)

print(response.status_code)
with open("demofile.txt", "a") as f:
  f.write(response.text)
