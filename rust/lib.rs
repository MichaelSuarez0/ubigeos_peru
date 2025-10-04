// use pyo3::prelude::*;
// use std::collections::HashMap;
// use once_cell::sync::Lazy;
// use rayon::prelude::*;
// use numpy::PyArray1;
// // use std::time::Instant;
// use pyo3::types::PyModule;

// #[pyfunction]
// fn get_departamento<'py>(py: Python<'py>, ubigeos: Vec<String>) -> PyResult<Bound<'py, PyArray1<Py<PyAny>>>> {
//     static DEPARTAMENTOS: Lazy<HashMap<&'static str, &'static str>> = Lazy::new(|| {
//         HashMap::from([
//             ("01", "Amazonas"),
//             ("02", "Áncash"),
//             ("03", "Apurímac"),
//             ("04", "Arequipa"),
//             ("05", "Ayacucho"),
//             ("06", "Cajamarca"),
//             ("07", "Callao"),
//             ("08", "Cusco"),
//             ("09", "Huancavelica"),
//             ("10", "Huánuco"),
//             ("11", "Ica"),
//             ("12", "Junín"),
//             ("13", "La Libertad"),
//             ("14", "Lambayeque"),
//             ("15", "Lima"),
//             ("16", "Loreto"),
//             ("17", "Madre de Dios"),
//             ("18", "Moquegua"),
//             ("19", "Pasco"),
//             ("20", "Piura"),
//             ("21", "Puno"),
//             ("22", "San Martín"),
//             ("23", "Tacna"),
//             ("24", "Tumbes"),
//             ("25", "Ucayali"),
//         ])
//     });

//     // let start = Instant::now();

//     // Paso 1: paralelo sin GIL → Option<&str>
//     let names: Vec<Option<&str>> = ubigeos
//         .into_par_iter()
//         .map(|u| DEPARTAMENTOS.get(u.as_str()).copied())
//         .collect();

//     // Paso 2: con GIL → convertir a Py<PyAny> y NumPy
//     let py_objects: Vec<Py<PyAny>> = names
//         .into_iter()
//         .map(|opt| match opt {
//             Some(name) => name.into_pyobject(py).unwrap().into_any().unbind(),
//             None => py.None(),
//         })
//         .collect();

//     // let dur = start.elapsed();
//     // println!("Rust get_departamento (NumPy) took: {:?}", dur);

//     Ok(PyArray1::from_vec(py, py_objects).into())
// }

// #[pymodule]
// fn ubigeos_rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
//     m.add_function(wrap_pyfunction!(get_departamento, m)?)?;
//     Ok(())
// }

use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use numpy::{PyArray1, PyArrayMethods};
use rayon::prelude::*;

// #[derive(Hash, Eq, PartialEq, Debug)]
// enum Nivel {
//     Departamento,
//     Provincia,
//     Distrito,
// }

// let longitud: i8 = match nivel {
//     Nivel::Departamento => 2,
//     Nivel::Provincia => 4,
//     Nivel::Distrito => 6,
// };

/// Valida un código ubigeo y devuelve los primeros `longitud` dígitos como `i16`.
///
/// # Argumentos
/// * `codigo` - El código ubigeo en formato string, debe contener solo dígitos.
/// * `longitud` - La longitud de corte (normalmente 2, 4 o 6).
///
/// # Errores
/// Retorna un `PyValueError` si el código contiene caracteres no numéricos
/// o si no se puede convertir a número.
///
/// # Ejemplo
/// ```
/// let n = validate_codigo("230145", 2).unwrap();
/// assert_eq!(n, 23);
/// ```
fn validate_codigo(codigo: &str, longitud: u8) -> PyResult<String> {
    if !codigo.chars().all(|c: char| c.is_ascii_digit()) {
        return Err(PyValueError::new_err(
            "El código debe contener solo dígitos",
        ));
    }

    if codigo.len() > 6 {
        return Err(PyValueError::new_err(
            "No se aceptan códigos con más de 6 caracteres",
        ));
    }

    let mut codigo = codigo.to_string();

    codigo = match codigo.len() {
        1 => format!("{:0>2}", codigo),
        3 => format!("{:0>4}", codigo),
        5 => format!("{:0>6}", codigo),
        _ => codigo,
    };

    let codigo_validado: String = codigo.chars().take(longitud as usize).collect();
    Ok(codigo_validado)
}

/// TODO: optimizar esta función para que acepte arrays de NumPy directamente.
#[pyfunction]
fn get_departamento_codes<'py>(
    py: Python<'py>,
    ubigeos: Vec<String>,
) -> PyResult<Vec<String>> {
    let longitud: u8 = 2;
    
    let codes: Vec<String> = ubigeos
        .par_iter()
        .map(|u| {
            validate_codigo(u, longitud).unwrap_or_else(|_| String::from("-1"))
        })
        .collect();

    Ok(codes)
}


#[pymodule]
fn ubigeos_rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_departamento_codes, m)?)?;
    Ok(())
}
