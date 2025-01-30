import streamlit as st
from openai import OpenAI
import json

# OpenAI API 설정
openai_api_key = st.text_input("OpenAI API Key", type="password")
st.title("👔 남성 패션 코디 추천")
st.write("당신에게 어울리는 스타일을 추천해드려요!")

# 사용자 정보 입력
age = st.number_input("나이를 입력하세요", min_value=0, value=30)
body_shape = st.selectbox("자신과 가까운 체형을 선택하세요", options=["슬림", "평균", "듬직", "근육질"])
height = st.number_input("키를 입력하세요 (cm)", min_value=100, value=175)
weight = st.number_input("몸무게를 입력하세요 (kg)", min_value=30, value=70)
preferred_style = st.selectbox("선호하는 스타일을 선택하세요", options=["비즈니스 캐주얼", "포멀", "캐주얼", "스트릿", "스포티", "아메리칸 캐주얼"])

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)
    
    submitted = st.button("코디 추천 받기")
    
    if submitted:
        with st.spinner("패션 코디 생성 중..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """
                        당신은 남성 패션 전문가입니다. 사용자의 체형, 선호하는 스타일, 키와 몸무게를 고려하여 가장 적합한 코디 세트를 추천해주세요.

                        응답 형식 (JSON):
                        {
                            "firstCoordination": {
                                "outer": "아우터 추천",
                                "top": "상의 추천",
                                "bottom": "하의 추천",
                                "description": "해당 코디에 대한 설명"
                            },
                            "secondCoordination": { ... },
                            "thirdCoordination": { ... }
                        }

                        스타일 가이드를 참고하여 코디를 추천하세요:
                        <style_guide>
                        {
                            "비즈니스 캐주얼": {
                                "아우터": ["코트", "자켓", "블레이저"],
                                "상의": ["셔츠", "니트", "티셔츠", "가디건"],
                                "하의": ["슬랙스"],
                                "style_description": "비즈니스 캐주얼 스타일은 단정하면서도 깔끔한 느낌을 강조하는 룩입니다."
                            },
                            "포멀": { ... },
                            "캐주얼": { ... },
                            "스트릿": { ... },
                            "스포티": { ... },
                            "아메리칸 캐주얼": { ... }
                        }
                        </style_guide>

                        색상 가이드를 참고하여 조합하세요:
                        <color_guide>
                        {
                            "밝은색상": ["화이트", "베이지", "라이트블루", "연청"],
                            "어두운색상": ["네이비", "블랙", "진청", "흑청", "브라운"],
                            "중간색상": ["그레이", "카키", "블루", "레드", "옐로우"]
                        }
                        </color_guide>
                        """
                    },
                    {
                        "role": "user",
                        "content": f"""
                        사용자 정보:
                        - 나이: {age}
                        - 체형: {body_shape}
                        - 키: {height}cm
                        - 몸무게: {weight}kg
                        - 선호 스타일: {preferred_style}
                        """
                    }
                ],
                response_format={"type": "json_object"}
            )
            
            recommendations = json.loads(response.choices[0].message.content)
            
            st.subheader("추천된 코디")
            for i, key in enumerate(recommendations.keys()):
                st.write(f"### 코디 {i+1}")
                st.write(f"- **아우터**: {recommendations[key]['outer']}")
                st.write(f"- **상의**: {recommendations[key]['top']}")
                st.write(f"- **하의**: {recommendations[key]['bottom']}")
                st.write(f"📌 {recommendations[key]['description']}")
                st.write("---")
