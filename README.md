# SemiSupervisedLabler
SemiSupervisedLabler는 다양한 ML 모델을 사용해서 어떤 모델이 저희의 labeling에 사용할 수 있을 지 확인한 코드가 담겨있는 레포입니다.

TransE가 예측한 triple을 전부 신뢰할 수 없었기 때문에 정말 이 triple을 선후관계 예측에 사용할지 결정해야 했습니다.
수작업으로 모든 triple에 label을 달려고 했으나, 개수가 너무 많아 그렇게까지는 하지 못했고,
1000여 개의 semi-supervised learning으로 전체 triple 중 어떤 triple을 사용할 지 예측하려고 했습니다.

Logistic Regression, Soft margin SVM, Naive Bayes Classifier, Random Forest Classifier를 사용했으며,
그 중 Random Forest가 가장 성능이 가장 좋음을 확인했습니다.
