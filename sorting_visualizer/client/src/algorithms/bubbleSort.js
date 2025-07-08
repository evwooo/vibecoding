export const bubbleSort = (array) => {
    const animations = [];
    let n = array.length;
    for (let i = 0; i < n - 1; i++) {
        for (let j = 0; j < n - i - 1; j++) {
            animations.push([j, j + 1]);
            animations.push([j, j + 1]);
            if (array[j] > array[j + 1]) {
                animations.push([j, array[j + 1], j + 1, array[j]]);
                [array[j], array[j + 1]] = [array[j + 1], array[j]];
            } else {
                animations.push([-1, -1]);
            }
        }
    }
    return animations;
};

export const bubbleSortCode = `
function bubbleSort(arr) {
  let n = arr.length;
  for (let i = 0; i < n - 1; i++) {
    for (let j = 0; j < n - i - 1; j++) {
      if (arr[j] > arr[j + 1]) {
        [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
      }
    }
  }
  return arr;
}
`;
