## 🚀 Executive Summary
This project focuses on developing a machine learning model to predict optimal poker strategies (Call, Raise, Fold) based on in-game observations. 
Using a dataset containing player statistics, game metrics, and card details, explored multiple models, including Logistic Regression, Neural Networks, and XGBoost.

Through data preprocessing and feature engineering, key predictors such as card ranks, card suits, and action, were prepared for analysis. Polynomial transformations and hyperparameter tuning were applied to enhance model performance.

After evaluation using accuracy metric and confusion matrices, the XGBoost was selected as the final model due to its superior ability to capture non-linear relationships and complex interactions within the data. The model was deployed using Streamlit, offering an interactive interface for real-time decision-making recommendations.

This project demonstrates the value of machine learning in strategic decision-making and provides a foundation for integrating advanced tools into poker strategy optimization. Future work will explore more advanced models and real-time applications for live gameplay analysis.

## 📘 Data Dictionary


| **Field Name**         | **Description**                                                                                                                                           |
|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `game_id`              | Unique identifier for each game (UUID)                                                                                                                     |
| `hand_id`              | The current round count (hand_id)                                                                                                                          |
| `round_index`          | The current street (e.g., pre-flop, flop, turn, river)                                                                                                     |
| `player_name`          | The name of the player taking the action                                                                                                                   |
| `action`               | The action taken by the player (e.g., 'call', 'raise', 'fold')                                                                                           |
| `amount`               | The amount of money involved in the action (for raise or call)                                                                                             |
| `hole_cards`           | Hole cards of the player, represented as a string of card values (e.g., '2H-3D') if available                                                            |
| `community_cards`      | Community cards at that point in the round, represented as a string of card values (e.g., '5H-7S-9C')                                                    |
| `pot`                  | The total amount of money in the pot at that point                                                                                                         |
| `player_stack`         | The remaining stack of the player after the action                                                                                                        |
| `small_blind`          | The small blind amount                                                                                                                                    |
| `big_blind`            | The big blind amount                                                                                                                                      |
| `winner`               | The winner of the round (empty until determined at the round's end)                                                                                      |

--------------------------------------------------------------------------------------------------------------------------------------------------------------

## 📊 Modeling Performance Insight:

I have run a total of 3 models:

1. Logistic Regression
2. Neural Network
3. XGBoost

The results in all 3 models show at least 40% accuracy, which perform over baseline accuracy (38%).

The XGBoost model, before applying the best parameters, achieves an accuracy of **58%**. After applying the best parameters, the accuracy changes to **57%**. Although the accuracy is slightly lower after applying the best parameters, the model performs better in terms of handling overfitting.

This is a _notable improvement_ compared to the Logistic Regression model **42%** and the Neural Network model **47%**. 


### 📍 Logistic Regression Performance
### Accuracy **42%**

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| 0     | 0.31      | 0.23   | 0.26     | 622     |
| 1     | 0.46      | 0.69   | 0.55     | 737     |
| 2     | 0.43      | 0.21   | 0.29     | 414     |


---
### 📍 Neural Netwok Performance
### Accuracy **46%**

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| 0     | 0.35      | 0.30   | 0.32     | 622     |
| 1     | 0.54      | 0.58   | 0.56     | 737     |
| 2     | 0.46      | 0.51   | 0.48     | 414     |


---
### 📍 XGBoost Model Performance
### Accuracy **57%**

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| Call  | 0.59      | 0.45   | 0.51     | 622     |
| Raise | 0.67      | 0.62   | 0.65     | 737     |
| Fold  | 0.43      | 0.65   | 0.52     | 414     |

## 📋 Conclusion About the Project

This project aimed to predict optimal poker strategies—Call, Raise, or Fold—using advanced machine learning models. Based on the findings:

1. **Model Selection**: 
**XGBoost** achieved the highest accuracy (57%), demonstrating its ability to handle the complexity of the dataset effectively. Other models, such as Logistic Regression and Neural Networks, showed lower performance.

2. **Class-Specific Insights**:
The model performs best for **Class 1 (Raise)**, with the highest precision and recall, suggesting that the dataset captures features that are more predictive of this action. **Class 0 (Call)** and **Class 2 (Fold)** show weaker performance, indicating potential challenges in distinguishing these actions based on the provided features.

3. **Feature Relevance**:
The inclusion of strategic poker features such as pot size and player stack sizes contributed to the model's predictive power. However, further exploration of feature engineering (e.g., interaction terms or additional contextual information) may improve predictions.

4. **Practical Application**:
The model provides valuable recommendations to players for making optimal decisions in poker games. While its accuracy is not perfect, it offers a baseline strategy that can be refined further through additional data and model tuning.

5. **Future Directions**:
Improving the dataset by including more real-world poker scenarios or advanced domain-specific features or model could enhance accuracy.
