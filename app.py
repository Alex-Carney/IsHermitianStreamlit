import streamlit as st
import numpy as np
from enum import Enum

class MatrixType(Enum):
    UNITARY = "Unitary"
    HERMITIAN = "Hermitian"
    NONE = "None"

def classify_matrix(matrix: np.array) -> [MatrixType]:
    classifications = []
    if np.allclose(matrix, matrix.T.conj()):
        classifications.append(MatrixType.HERMITIAN)
    if np.allclose(matrix @ matrix.T.conj(), np.eye(matrix.shape[0])):
        classifications.append(MatrixType.UNITARY)
    if len(classifications) == 0:
        classifications.append(MatrixType.NONE)
    return classifications

def convert_to_complex(input_str):
    input_str = input_str.strip().lower().replace(' ', '')
    if input_str == 'i':
        return complex(0, 1)
    elif input_str == '-i':
        return complex(0, -1)
    return complex(input_str)

st.title("Matrix Classifier")
st.write("Select an example matrix or enter complex numbers manually. When you are ready, click 'Classify Matrix' to determine if the matrix is unitary and/or Hermitian.")
st.write("Note that complex numbers should be entered in the form 'a+bj' or 'a-bj' where 'j' is the imaginary unit. For example, '3+2j' or '1-4j'.")

# Example matrices for 2x2
pauli_x = np.array([[0, 1], [1, 0]])
pauli_y = np.array([[0, -1j], [1j, 0]])
pauli_z = np.array([[1, 0], [0, -1]])
neither_matrix = np.array([[2, 1], [3, 4]])  # Example that is neither unitary nor Hermitian

examples = {
    "Identity": np.eye(2),
    "Pauli X": pauli_x,
    "Pauli Y": pauli_y,
    "Pauli Z": pauli_z,
    "Neither Unitary Nor Hermitian": neither_matrix
}

# Select the size of the matrix
matrix_size = st.selectbox("Select the size of the matrix:", options=[2, 3, 4, 5], index=0)

# Conditionally display examples for size 2
if matrix_size == 2:
    selected_example = st.selectbox("Load example matrix:", options=list(examples.keys()), index=0)
    example_matrix = examples[selected_example]
else:
    selected_example = None
    example_matrix = np.eye(matrix_size)  # Default to identity matrix for sizes greater than 2

# Generate the grid of input fields
matrix_input = []
for i in range(matrix_size):
    cols = st.columns(matrix_size)  # create a row of input columns
    row = []
    for j in range(matrix_size):
        with cols[j]:
            # Set the default value based on selected example or identity
            default_value = str(example_matrix[i][j]) if selected_example or matrix_size > 2 else "0"
            elem = st.text_input(f"Element ({i+1},{j+1})", value=default_value, key=f"cell-{i}-{j}-{selected_example}-{matrix_size}")
            row.append(elem)
    matrix_input.append(row)

# When the user submits the matrix
if st.button('Classify Matrix'):
    try:
        complex_matrix = np.array([[convert_to_complex(item) for item in row] for row in matrix_input], dtype=complex)
        classification = classify_matrix(complex_matrix)
        st.write("The matrix is classified as:")
        for class_type in classification:
            st.write(class_type.value)
    except ValueError as e:
        st.error("Invalid input. Please ensure all matrix elements are in the correct complex format.")
