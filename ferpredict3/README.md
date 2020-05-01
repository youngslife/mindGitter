# Facial Emotion Recognition Model

[TOC]

## References

- stanford, emotion reckon in narration 2019 

  [file:///C:/Users/com/Downloads/1912.05008.pdf](file:///C:/Users/com/Downloads/1912.05008.pdf)

- brief review (~2017) 
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5856145/#B13-sensors-18-00401

- 78 % accuracy (2017)
https://www.researchgate.net/profile/Wissam_Baddar/publication/316265893_Multi-Objective_based_Spatio-Temporal_Feature_Representation_Learning_Robust_to_Expression_Intensity_Variations_for_Facial_Expression_Recognition/links/59f879300f7e9b553ec0b06c/Multi-Objective-based-Spatio-Temporal-Feature-Representation-Learning-Robust-to-Expression-Intensity-Variations-for-Facial-Expression-Recognition.pdf

- 77 % accuracy (2016)
  https://arxiv.org/pdf/1511.04110.pdf

- 2015 

  https://m.blog.naver.com/PostView.nhn?blogId=creative_ct&logNo=220556682640&proxyReferer=https:%2F%2Fwww.google.com%2F



## Reviews

### Multi Object (2017) 

- 비디오 영상 내 사용자의 연속적인 표정의 변화와 미묘한 표정차이를 분석하는데 이점
- Modeling Emotion (2019) 가 긍부정인 상태를 예측하는데 반해 다양한 감정 변화(7가지)를  예측하고 있음
- 다양한 감정이 있다는 것은 좋으나 이야기하는 상황을 가정하지 않음. 즉 입모양의 변화로 인해 예측의 정확성이 떨어질 수 있음 
- 에러텀을 직접 구현하는 것 외엔 까다롭지 않음
- 특정 표정의 시작과 끝을 기준으로 영상이 잘라져있어야함. 즉 데이터의 가공이 필요하다는게 치명적인 단점
  - 감정의 시작점과 고점, 끝점을 구별
  - 즉 7가지 종류의 표정의 강도를 구별
  - 고점을 기준으로 normalized cross correlation을 구해 비교



### Modeling emotion in complex stories(2019)

- 화자가 자신의 이야기를 하는 동안의 나타나는 긍부정 감정의 변화 데이터셋

- 이야기하는 동안의 자연스러운 감정 변화를 분석한다는 점에서 프로젝트에 더 부합

- 가공된 데이터가 아니라 narrative 영상에서 감정을 분석

  - 긍정 또는 부정 두 가지의 방향에서의 강도를 구별

  - Evaluator Weighted Estimator을 통해..?
  - Concordance Correlation Coefficient 를 통해 검증
  - LSTM 모델이 괜찮음

- Multi Object보다 상대적으로 복잡함

- file:///C:/Users/com/Downloads/2019_Wu_ACII_Attention_Transformer.pdf 은 transformer 버전인 것 같은 느낌적인 느낌



## Datasets

- MMI dataset : https://mmifacedb.eu/accounts/register/

- CASME dataset : http://fu.psych.ac.cn/CASME/casme2-en.php
  
  - https://github.com/bioidiap/bob.db.casme2 ..?
  
- SEND (요청 해둔 상태)

- http://www.cse.oulu.fi/wsgi/SMICDatabase?action=AttachFile&do=view&target=SMIC+database+description_full+version

- https://avec2013-db.sspnet.eu/accounts/register/

  



## Plan

- 영상의 연속적인 표정 변화를 구별해낼 수 있는 모델을 구현하기 위해선

  - 일단 감정이 라벨링된 **영상 데이터셋들을 확보해**야하고
  - 전체 영상에서 특징이 되는 표정을 단위로 나뉘는 가공이 필요하며
  - 레퍼런스들에서 필요에 따라 모델을 커스터마이징 해야한다.
  
- 가장 간단한 모델을 구현하고 이후 연구한 모델로 바꾸기

  - 기본 표정 분류 모델

    - 정면사진으로 훈련/테스트 (4/16 - 4/17)
    - 영상에서 추출된 프레임으로 테스트(4/20)

  - 영상의 연속적인 표정 변화를 구별해낼 수 있는 모델

    - LSTM (SEND dataset) 모델 (standford 2019 참고)
    
    

## Basic Structure

- config
- preprocessing
  - picture / frames from videos
  - face detection (if necessary)
  - audio extraction
  - **audio to text (google sst api)**
- data augment 
- cnn or (cnn + lstm)
- checkpoint
- train & validation
- test & visualization
- rest api



- send 데이터 다른 사람도 요청 부탁
- 건호쓰에게 data augment부분 + vanila rest api 부분 부탁
- 윤영쓰 구글 sst api 코드 부탁

