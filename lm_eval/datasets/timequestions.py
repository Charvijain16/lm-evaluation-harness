import json
from datetime import datetime

out_path = '/home/charvi-jain/RINO/temporal_datasets/TimeQestions_EXAQT/test_processed.json'
with open('/home/charvi-jain/RINO/temporal_datasets/TimeQestions_EXAQT/test.json', 'r') as f:
    count = 0
    json_lines=json.load(f)
    docs = []
    for line in json_lines:
        doc = {}
        answers = []
        for ans in line["Answer"]:
            a=ans.get("AnswerArgument", None) or ans.get("WikidataLabel", None)
            new_date = None
            try:
                date = datetime.strptime(a, "%Y-%m-%dT%H:%M:%SZ")
                new_date = date.strftime('%b, %Y')
            except ValueError:
                pass
            
            if new_date != None:
                a = new_date
            answers.append(a)
        doc['question'] = line['Question']
        question_creation_date = datetime.strptime(line['Question creation date'], "%Y-%m-%d")
        doc['date'] = question_creation_date.strftime('%B %d, %Y')
        doc['text_answers'] = answers
        doc['question_type'] = line["Temporal question type"]
        if len(answers) == 0:
            count+=1
        else:
            docs.append(doc)
    print(count, len(json_lines))
    
f.close()
with open(out_path, 'w') as f1:
    print(f"Storing data as JSONL in {out_path} ...")
    print(len(docs))
    for entry in docs:
        json_str = json.dumps(entry, ensure_ascii=False)
        f1.write(json_str + "\n")
 
print('Done')