export const quickSort = (array) => {
    const animations = [];
    quickSortHelper(array, 0, array.length - 1, animations);
    return animations;
};

function quickSortHelper(array, low, high, animations) {
    if (low < high) {
        const pi = partition(array, low, high, animations);
        quickSortHelper(array, low, pi - 1, animations);
        quickSortHelper(array, pi + 1, high, animations);
    }
}

function partition(array, low, high, animations) {
    const pivot = array[high];
    let i = low - 1;
    for (let j = low; j < high; j++) {
        animations.push([j, high]);
        animations.push([j, high]);
        if (array[j] < pivot) {
            i++;
            animations.push([i, array[j], j, array[i]]);
            [array[i], array[j]] = [array[j], array[i]];
        } else {
            animations.push([-1, -1]);
        }
    }
    animations.push([i + 1, array[high], high, array[i + 1]]);
    [array[i + 1], array[high]] = [array[high], array[i + 1]];
    return i + 1;
}

export const quickSortCode = `
function quickSort(arr, low, high) {
  if (low < high) {
    let pi = partition(arr, low, high);
    quickSort(arr, low, pi - 1);
    quickSort(arr, pi + 1, high);
  }
  return arr;
}

function partition(arr, low, high) {
  let pivot = arr[high];
  let i = low - 1;
  for (let j = low; j < high; j++) {
    if (arr[j] < pivot) {
      i++;
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
  }
  [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]];
  return i + 1;
}
`;
