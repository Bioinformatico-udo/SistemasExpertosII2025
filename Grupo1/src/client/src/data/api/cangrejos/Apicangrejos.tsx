import axios from 'axios'

export const CRAB_SPECIES = [
  { 'id': 1, 'nombre_cientifico': 'Neopisosoma_neglectum', 'nombre_display': 'Neopisosoma neglectum', 'image': 'images/crab/caparazon_rugoso.jpg' },
  { 'id': 2, 'nombre_cientifico': 'Neopisosoma_angustifrons', 'nombre_display': 'Neopisosoma angustifrons', 'image': 'images/crab/caparazon_rugoso.jpg' },
  { 'id': 3, 'nombre_cientifico': 'Neopisosoma_orientale', 'nombre_display': 'Neopisosoma orientale', 'image': 'images/crab/caparazon_rugoso.jpg' },
  { 'id': 4, 'nombre_cientifico': 'Clastotoechus_nodosus', 'nombre_display': 'Clastotoechus nodosus', 'image': '/imagenes/cangrejos/Clastotoechus_nodosus.png' },
  { 'id': 5, 'nombre_cientifico': 'Pachycheles_serratus', 'nombre_display': 'Pachycheles serratus', 'image': 'images/crab/caparazon_rugoso.jpg' },
  { 'id': 6, 'nombre_cientifico': 'Pachycheles_monilifer', 'nombre_display': 'Pachycheles monilifer', 'image': 'images/crab/caparazon_rugoso.jpg' },
  { 'id': 7, 'nombre_cientifico': 'Pachycheles_riseii', 'nombre_display': 'Pachycheles riseii', 'image': 'images/crab/caparazon_rugoso.jpg' },
  { 'id': 8, 'nombre_cientifico': 'Pachycheles_ackleianus', 'nombre_display': 'Pachycheles ackleianus', 'image': 'images/crab/caparazon_rugoso.jpg' },
  { 'id': 9, 'nombre_cientifico': 'Petrolisthes_tridentatus', 'nombre_display': 'Petrolisthes tridentatus', 'image': 'images/crab/caparazon_rugoso.jpg' },
];
const URL_API = 'http://127.0.0.1:5000/cangrejos';
const datosAEnviar = {
  "elementos": [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
};


export async function enviarDatosAxios(datos: Array<Number> = [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0]): Promise<string> {
  let respuestaServidorString: string = '';
  const datosAEnviar = {
    "elementos": datos,
  };

  try {
    console.log('Enviando datos al servidor:', datosAEnviar);
    const respuesta = await axios.post(URL_API, datosAEnviar, {
    });
    const especieCientifica = respuesta.data.cangrejo;


    // 2. Buscar la especie en el array CRAB_SPECIES
    const especieEncontrada = CRAB_SPECIES.find(
      (especie) => especie.nombre_cientifico === especieCientifica
    );
    console.log('Datos enviados correctamente:', respuesta.data.cangrejo);
    return especieEncontrada ? especieEncontrada.nombre_display : 'Especie no encontrada';



  } catch (error) {
    console.error('Hubo un problema con la petición POST:', error);
    return 'Error en la petición';
  }
}



