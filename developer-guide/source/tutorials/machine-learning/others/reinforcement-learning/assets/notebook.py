import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

n_estimators_options = np.arange(50, 201, 50)
max_depth_options = np.arange(1, 11)

q_table = np.zeros((len(n_estimators_options), len(max_depth_options)))

epsilon = 0.1   # probability of exploration (vs. exploitation)
alpha = 0.1     # learning rate
gamma = 0.9     # discount factor (importance of future rewards)
episodes = 50

for episode in range(episodes):
    # Choose an initial state with random hyper parameters
    ne_idx = np.random.randint(len(n_estimators_options))
    md_idx = np.random.randint(len(max_depth_options))

    for step in range(10):  # Limit the number of steps per episode
        # Epsilon greedy action selection
        if np.random.rand() < epsilon:
            # Explore: choose random hyper parameters
            ne_idx_new = np.random.randint(len(n_estimators_options))
            md_idx_new = np.random.randint(len(max_depth_options))
        else:
            # Exploit: choose the hyper parameters with the highest Q value so far
            ne_idx_new, md_idx_new = np.unravel_index(np.argmax(q_table), q_table.shape)

        # Train model with the selected hyper parameters
        model = RandomForestClassifier(
            n_estimators = int(n_estimators_options[ne_idx_new]),
            max_depth = int(max_depth_options[md_idx_new])
        )
        model.fit(X_train, y_train)

        # Evaluate model on the validation set
        y_pred = model.predict(X_val)
        accuracy = accuracy_score(y_val, y_pred)

        # Update the Q value; here the reward is the accuracy
        q_table[ne_idx, md_idx] = q_table[ne_idx, md_idx] + alpha * (
            accuracy + gamma * np.max(q_table[ne_idx_new, md_idx_new]) - q_table[ne_idx, md_idx]
        )

        # Move to the next state
        ne_idx, md_idx = ne_idx_new, md_idx_new

best_ne_idx, best_md_idx = np.unravel_index(np.argmax(q_table), q_table.shape)
best_n_estimators = n_estimators_options[best_ne_idx]
best_max_depth = max_depth_options[best_md_idx]

print("Best Number of Estimators:", best_n_estimators)
print("Best Max Depth:", best_max_depth)

best_model = RandomForestClassifier(
    n_estimators = int(best_n_estimators),
    max_depth = int(best_max_depth)
)
best_model.fit(X, y)