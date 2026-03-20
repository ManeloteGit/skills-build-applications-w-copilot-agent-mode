import React from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const NotFound = () => {
  return (
    <Container>
      <Row className="justify-content-center align-items-center" style={{ minHeight: '70vh' }}>
        <Col md={6} className="text-center">
          <h1 className="display-1 fw-bold">404</h1>
          <h2 className="mb-4">Página No Encontrada</h2>
          <p className="lead mb-4">
            Parece que la página que buscas no existe o ha sido removida.
          </p>
          <Link to="/" className="btn btn-primary btn-lg">
            Volver al Inicio
          </Link>
        </Col>
      </Row>
    </Container>
  );
};

export default NotFound;
