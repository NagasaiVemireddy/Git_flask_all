def linear_search(nums, target):
    """
    Returns index of target if found, else -1
    """
    for i, value in enumerate(nums):
        if value == target:
            return i
    return -1


if __name__ == "__main__":
    data = [10, 20, 30, 40, 50]
    print(linear_search(data, 30))  # expected output: 2
