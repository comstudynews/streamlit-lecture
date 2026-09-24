# Step 05 - Dictionary Chain

## 목표
사용자의 일상 표현을 문서 검색에 적합한 표현으로 정규화합니다.

## 실행
```bash
python step05_dictionary_chain/complete/dictionary_demo.py
```

## 핵심
`prompt | llm | StrOutputParser()`는 LCEL로 앞 단계의 결과를 다음 단계에 전달합니다.
