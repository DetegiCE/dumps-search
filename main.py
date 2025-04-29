from parser import prepare_parser
from googlesearch import search

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

EXAM = {
    "aws-scs": {
        "query": "examtopic aws certified security specialty topic 1 question",
        "keyword": "aws-certified-security-specialty-topic-1-question",
    },
    "gcp-ace": {
        "query": "examtopic gcp ace question",
        "keyword": "associate-cloud-engineer-topic-1-question",
    },
    "ai-900": {
        "query": "examtopic ai 900 question",
        "keyword": "ai-900-topic-1-question",
    },
    "saa-c03": {
        "query": "examtopic saa c03 question",
        "keyword": "exam-aws-certified-solutions-architect-associate-saa-c03",
    },
    "clf-c02": {
        "query": "examtopics aws certified cloud practitioner clf c02 topic 1 question",
        "keyword": "exam-aws-certified-cloud-practitioner-clf-c02-topic-1",
    },
    "aif-c01": {
        "query": "ai practitioner examtopics questions topic 1 question",
        "keyword": "exam-aws-certified-ai-practitioner-aif-c01-topic-1-question"
    }
}


def get_answer_url(exam_id, index):
    query = f"{EXAM[exam_id]['query']} {index}"
    print(query)
    try:
        result_urls = list(search(query, num_results=100, sleep_interval=1))
    except:
        result_urls = []
    print(result_urls)
    
    for url in result_urls:
        if f"{EXAM[exam_id]['keyword']}-{index}" in url:
            print(f"Found URL for question #{index}: {url}")
            return url

    for url in result_urls:
        if f"{EXAM[exam_id]['keyword']}" in url:
            print(f"Found URL for question #{index}: {url}")
            return url
    return None

def html_template(result_urls, exam_id):
    return f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{exam_id}</title>
    <style>

    </style>
</head>
<body>
    <div id="container">
        <div id="number" style="background-color: white; z-index: 9999; display: flex; justify-content: center; align-items: center; position: fixed; left: 0; top: 0; width: 100%; height: 100px; font-size: 40px;">
            <span><button id="start" onclick="notworking()" style="font-size: 20px;">START<br>NOT WORKING</button></span>
            <span><button id="prev" onclick="prev()"style="font-size: 20px;">&lt;</button></span>
            <span id="currentNumber">1</span>
            <span>/{len(result_urls)-1}</span>
            <span><button id="next" onclick="next()"style="font-size: 20px;">&gt;</button></span>
            <input type="number" name="jumpnum" id="jumpnum" min="1" max="{len(result_urls)-1}" style="margin-left: 20px">
            <button id="jumpbtn" onclick="jump()"style="font-size: 20px;">JUMP!</button>
        </div>
        <div id="loading" style="text-align: center; font-size: 24px; color: red; margin-top: 110px;"></div>
        <div id="innerFrame" width="50%" height="600px"></div>
    </div>
    <script>
        let problems = {str(result_urls)};
        function gethtml(url) {{
            console.log(url);
            if(url.includes('None')) {{
                console.log('None', url.includes('None'));
                document.getElementById("innerFrame").innerHTML = "<div style='color:red;'>Sorry, URL not found.</div>";
                return;
            }}
            else {{
                console.log('Start', url.includes('None'));
                document.getElementById("loading").innerText = 'Loading...';
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.onreadystatechange = function() {{
                if(xmlHttp.status == 200 && xmlHttp.readyState == xmlHttp.DONE) {{
                    console.log(JSON.parse(xmlHttp.responseText)['contents']);
                    let contents = JSON.parse(xmlHttp.responseText)['contents'].replaceAll('href="/', 'href="https://www.examtopics.com/')
                    contents = contents.replaceAll('src="/', 'src="https://www.examtopics.com/')
                    contents = contents.replace('class="card-text question-answer bg-light white-text"', 'class="card-text question-answer bg-light white-text" style="display: block;"')
                    
                    let footerStart = contents.indexOf('<!-- Footer Start -->');
                    let footerEnd = contents.indexOf('<!-- Footer End -->');
                    let afterFooter = contents.substring(footerEnd);
                    let beforeFooter = contents.substring(0, footerStart);
                    contents = beforeFooter + afterFooter;
                    
                    let headerStart = contents.indexOf('<!--Header Start-->');
                    let headerEnd = contents.indexOf('<!--Header End-->');
                    let afterHeader = contents.substring(headerEnd);
                    let beforeHeader = contents.substring(0, headerStart);
                    contents = beforeHeader + afterHeader;

                    contents = contents.replaceAll('<div class="container">', '<div class="container">AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')

                    let adStart = contents.indexOf('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA');
                    let adEnd = contents.indexOf('<!-- BEGIN Discussions header / title -->');
                    let afterAD = contents.substring(adEnd);
                    let beforeAD = contents.substring(0, adStart);
                    contents = beforeAD + afterAD;

                    contents = contents.replace('<div class="rs-toolbar">', '<div class="rs-toolbar" style="background-color: white;">')
                    contents = contents.replace('<link rel="stylesheet" type="text/css" href="https://www.examtopics.com/assets/css/style.css?ver=1">', '')

                    document.getElementById("innerFrame").innerHTML = contents;
                    document.getElementById("loading").innerText = '';
                    return;
                }}
            }};

            xmlHttp.open('GET', url, true);

            xmlHttp.send();
            }}
            
        }}
        function notworking() {{
            let curNum = Number(document.getElementById("currentNumber").innerText);
            gethtml(problems[curNum]);
        }}
        function prev() {{
            let curNum = Number(document.getElementById("currentNumber").innerText);
            if(curNum == 1) {{
                alert("Can't go back");
            }}
            else {{
                document.getElementById("currentNumber").innerText = curNum - 1;
                gethtml(problems[curNum-1]);
            }}
        }}
        function next() {{
            let curNum = Number(document.getElementById("currentNumber").innerText);
            if(curNum == problems.length-1) {{
                alert("Can't go next");
            }}
            else {{
                document.getElementById("currentNumber").innerText = curNum + 1;
                gethtml(problems[curNum+1]);
            }}
        }}
        function jump() {{
            let jumppage = Number(document.getElementById("jumpnum").value);
            document.getElementById("currentNumber").innerText = jumppage;
            gethtml(problems[jumppage]);
        }}
    </script>
</body>
</html>
    """

if __name__ == "__main__":
    options = prepare_parser().parse_args()
    result_urls = ['',]

    for index in range(options.start, options.end + 1):
        ansurl = get_answer_url(options.exam, index)
        result_urls.append('https://api.allorigins.win/get?url='+str(ansurl))
        print(index, result_urls[-1])

    html = html_template(result_urls, options.exam)
    
    f = open(f'{options.exam}.html', 'w')
    f.write(html)
    f.close()
