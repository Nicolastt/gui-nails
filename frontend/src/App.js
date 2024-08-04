import React, { useState, useCallback, useRef } from 'react';
import axios from 'axios';
import { Alert, Col, Container, Row } from 'reactstrap';
import './styles/App.css';
import "bootstrap/dist/css/bootstrap.min.css";
import Camera from './components/Camera';
import Carrusel from './components/Carrusel';

const App = () => {
    const [imageSrc, setImageSrc] = useState(null);
    const [prediction, setPrediction] = useState(null);
    const [error, setError] = useState(null);

    const webcamRef = useRef(null);

    const capture = useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        setImageSrc(imageSrc);
        sendImageToServer(imageSrc);
    }, [webcamRef]);

    const sendImageToServer = async (base64Image) => {
        try {
            const blob = convertBase64ToBlob(base64Image);
            const formData = new FormData();
            formData.append('image', blob, 'image.jpg');

            // Envía la imagen al servidor
            const response = await axios.post('http://localhost:5000/process-image', formData);

            if (response.status === 200) {
                console.log('Imagen enviada correctamente:', response.data);
                // Procesar la recomendación recibida
                fetchRecommendations(response.data.recommendation);
            } else {
                console.error('Respuesta de error:', response);
                setError('Hubo un problema al procesar la imagen.');
            }
        } catch (error) {
            console.error("Se ha producido un error al enviar la imagen!", error);
            setError("Se ha producido un error al enviar la imagen. Por favor, inténtelo de nuevo.");
        }
    };

    const fetchRecommendations = async (recommendation) => {
        try {
            const response = await axios.get(`http://localhost:5000/images/${recommendation}`);
            if (response.data.error) {
                setError(response.data.error);
                setPrediction(null);
            } else {
                setPrediction(response.data);
                setError(null);
            }
        } catch (error) {
            console.error("Se ha producido un error al obtener las recomendaciones!", error);
            setError("Se ha producido un error en la búsqueda de recomendaciones. Por favor, inténtelo de nuevo.");
            setPrediction(null);
        }
    };

    const convertBase64ToBlob = (base64Image) => {
        const [header, data] = base64Image.split(',');
        const mime = header.match(/:(.*?);/)[1];
        const binary = atob(data);
        const array = [];
        for (let i = 0; i < binary.length; i++) {
            array.push(binary.charCodeAt(i));
        }
        return new Blob([new Uint8Array(array)], { type: mime });
    };

    const handleRetake = () => {
        setPrediction(null); // Reinicia el estado de prediction al retomar la foto
    };

    return (
        <Container className="App">
            <h1 className="text-center my-4">Kdú Nails Art IA</h1>
            <h6 className="text-center">Resaltamos tu estilo y belleza</h6>
            <Row className="camera-container">
                <Col className="camera-wrapper">
                    <Camera
                        imageSrc={imageSrc}
                        setImageSrc={setImageSrc}
                        capture={capture}
                        webcamRef={webcamRef}
                        onRetake={handleRetake} // Pasa la función handleRetake
                    />
                    {prediction && <Carrusel />}
                </Col>
                {error && (
                    <Col md="12" className="d-flex justify-content-center">
                        <Alert color="danger">
                            {error}
                        </Alert>
                    </Col>
                )}
            </Row>
        </Container>
    );
};

export default App;
