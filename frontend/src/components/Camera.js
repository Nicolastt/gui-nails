import React from 'react';
import { Button, Card, CardBody, CardTitle } from 'reactstrap';
import Webcam from 'react-webcam';
import '../styles/Camera.css';
import "bootstrap/dist/css/bootstrap.min.css";

const Camera = ({ imageSrc, setImageSrc, capture, webcamRef, onRetake }) => {
    return (
        <Card className="camera-card mb-4 text-center">
            <CardBody>
                {!imageSrc ? (
                    <>
                        <Webcam
                            audio={false}
                            ref={webcamRef}
                            screenshotFormat="image/jpeg"
                            className="webcam-view"
                        />
                        <Button className="capture-btn mt-3" onClick={capture}>Capturar Foto</Button>
                    </>
                ) : (
                    <>
                        <CardTitle className="captured-title">Foto Capturada</CardTitle>
                        <img src={imageSrc} alt="Captured" className="captured-img" />
                        <Button className="retake-btn mt-3" onClick={() => {
                            setImageSrc(null);
                            onRetake();
                        }}>Retomar Foto</Button>
                    </>
                )}
            </CardBody>
        </Card>
    );
};

export default Camera;
