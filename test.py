with open("output.html", "r", encoding="utf-8") as file:
    content = file.read()

# print(content)

import re    

regex_patterns = {
"pattern_usdcnh": "<script\\s+data-sveltekit-fetched=\"\"\\s+data-ttl=\"1\"[\\s\\S]*?<\\/script>", 
"pattern_symbol": "\\\\\"symbol\\\\\":\\\\\".*?\\\\\"",
"pattern_time" : "\\\\\"regularMarketTime\\\\\":\\{.*?\\}",
"pattern_price": "\\\\\"regularMarketPrice\\\\\":\\{.*?\\}",
"pattern_change": "\\\\\"regularMarketChange\\\\\":\\{.*?\\}",
"pattern_change_percent": "\\\\\"regularMarketChangePercent\\\\\":\\{.*?\\}"
}

pattern_usdcnh = regex_patterns.get("pattern_usdcnh")
pattern_symbol = regex_patterns.get("pattern_symbol")
pattern_time = regex_patterns.get("pattern_time")
pattern_price = regex_patterns.get("pattern_price")
pattern_change = regex_patterns.get("pattern_change")
pattern_change_percent = regex_patterns.get("pattern_change_percent")

usdcnh_match = re.search(pattern_usdcnh, content, re.DOTALL).group(0).replace("\\","")
usdcnh_match_re = usdcnh_match.replace("\\","")
print(usdcnh_match_re)