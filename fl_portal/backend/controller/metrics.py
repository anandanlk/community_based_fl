import re

def generate_metrics(logs) -> dict:
    rounds = []
    training_accuracies = []
    testing_accuracies = []
    model_sizes = []
    # aggregation_time = []

    metrics = {
        "Round": rounds,
        "Training Accuracy": training_accuracies,
        "Testing Accuracy": testing_accuracies,
        "Model Size (MiB)": model_sizes,
        # "Aggregation Time per round": aggregation_time
    }

    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]') 
    logs = ansi_escape.sub('', logs)

    round_pattern = re.compile(r"INFO \[step decentralized_federated_learning_round_(\d+)\] completed success")
    train_acc_pattern = re.compile(r"Training accuracy: ([\d\.]+)")
    test_acc_pattern = re.compile(r"Testing accuracy: ([\d\.]+)")
    size_pattern = re.compile(r"INFO \[job receive_weights_\d+\] Max memory used: (\d+)MiB")
    # aggregation_time_pattern = re.compile(r"(\b\d+:\d{2}:\d{2}\b).*\nINFO \[job aggregation_")
    time_pattern = re.compile(r"(\d+m\d+\.\d+s)")

    for match in round_pattern.finditer(logs):
        rounds.append(int(match.group(1)))
        
    for match in train_acc_pattern.finditer(logs):
        training_accuracies.append(float(match.group(1)))
    
    for match in test_acc_pattern.finditer(logs):
        testing_accuracies.append(float(match.group(1)))
    
    for match in size_pattern.finditer(logs):
        model_sizes.append(int(match.group(1)))

    total_time_matches = time_pattern.findall(logs)
    if total_time_matches:
        total_time = total_time_matches[0]
    else:
        total_time = None

    return total_time, metrics
