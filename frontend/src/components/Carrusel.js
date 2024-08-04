import React, { useEffect, useState } from 'react';
import { Alert, Card, CardBody, Spinner } from 'reactstrap';
import axios from 'axios';
import '../styles/Carrusel.css';
import "bootstrap/dist/css/bootstrap.min.css";

const Carrusel = () => {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchRecommendation = async () => {
            try {
                const response = await axios.get('http://localhost:5000/recommendations');
                const recommendation = response.data.recommendation;

                const imagesResponse = await axios.get(`http://localhost:5000/images/${recommendation}`);
                const imageList = imagesResponse.data.images;

                const doubledItems = imageList.map((img, index) => ({
                    src: `http://localhost:5000/static/images/${recommendation}/${img}`,
                    key: index
                }));

                // Duplicar las imágenes para el efecto de carrusel infinito
                setItems([...doubledItems, ...doubledItems]);
            } catch (error) {
                console.error('Error fetching recommendation or images:', error);
                setError('Error fetching images. Please try again later.');
            } finally {
                setLoading(false);
            }
        };

        fetchRecommendation();
    }, []);

    if (loading) {
        return (
            <div className="text-center mt-4">
                <Spinner style={{ width: '3rem', height: '3rem' }} />
            </div>
        );
    }

    if (error) {
        return (
            <Alert color="danger" className="text-center mt-4">
                {error}
            </Alert>
        );
    }

    return (
        <Card className="mb-5 prediction-card mt-2 w-100">
            <CardBody className="mb-4 prediction-card-body mt-4 w-100">
                <h2 className="text-center mb-5">¡Te quedaría increíble uno de estos diseños!</h2>
                {items.length > 0 ? (
                    <div className="custom-carousel">
                        <div className="carousel-inner">
                            {items.map(item => (
                                <Card className="carousel-card" key={item.key}>
                                    <CardBody className="p-0">
                                        <img src={item.src} alt="Carousel item" className="carousel-image" />
                                    </CardBody>
                                </Card>
                            ))}
                        </div>
                    </div>
                ) : (
                    <Alert color="info" className="text-center">
                        Aún estamos buscando recomendaciones para ti...
                    </Alert>
                )}
            </CardBody>
        </Card>
    );
};

export default Carrusel;
