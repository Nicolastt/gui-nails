import React from 'react';
import {Col, Container, Row} from 'reactstrap';
import {FaFacebook, FaInstagram, FaTiktok, FaWhatsapp} from 'react-icons/fa';
import '../styles/Footer.css';

const Footer = () => {
    return (
        <footer className="footer">
            <Container>
                <Row className="align-items-center">
                    <Col md="12" className="text-center">
                        <a href="https://www.instagram.com/kdunails?igsh=bTIyYmF2cjVsbWc0" target="_blank"
                           rel="noopener noreferrer" className="social-icon">
                            <FaInstagram/>
                        </a>
                        <a href="https://www.facebook.com/kdunailspa" target="_blank" rel="noopener noreferrer"
                           className="social-icon">
                            <FaFacebook/>
                        </a>
                        <a href="https://www.tiktok.com/@kdunails?_t=8oYRksM93dl&_r=1" target="_blank"
                           rel="noopener noreferrer" className="social-icon">
                            <FaTiktok/>
                        </a>
                        <a href="https://api.whatsapp.com/send/?phone=593969919679&text=Hola%2C+me+pueden+ayudar&type=phone_number&app_absent=0"
                           target="_blank" rel="noopener noreferrer" className="social-icon">
                            <FaWhatsapp/>
                        </a>
                    </Col>
                </Row>
            </Container>
        </footer>
    );
};

export default Footer;
