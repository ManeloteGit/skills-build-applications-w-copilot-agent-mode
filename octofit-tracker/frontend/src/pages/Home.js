import React from 'react';
import { Container, Row, Col, Button, Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const Home = () => {
  const { isAuthenticated } = useAuth();

  return (
    <Container>
      <Row className="my-5">
        <Col md={6} className="d-flex flex-column justify-content-center">
          <h1 className="display-4 fw-bold mb-4">💪 Octofit Tracker</h1>
          <p className="lead mb-4">
            Tu aplicación de fitness personalizada. Registra tus actividades, 
            compite con tus amigos y recibe recomendaciones de entrenamiento 
            personalizadas.
          </p>
          <div className="d-flex gap-3">
            {isAuthenticated ? (
              <Link to="/dashboard" className="btn btn-primary btn-lg">
                Ir al Dashboard
              </Link>
            ) : (
              <>
                <Link to="/login" className="btn btn-primary btn-lg">
                  Iniciar Sesión
                </Link>
                <Link to="/register" className="btn btn-outline-primary btn-lg">
                  Registrarse
                </Link>
              </>
            )}
          </div>
        </Col>
        <Col md={6} className="d-flex justify-content-center align-items-center">
          <div className="text-center" style={{ fontSize: '120px' }}>
            🏃‍♂️
          </div>
        </Col>
      </Row>

      {!isAuthenticated && (
        <Row className="my-5">
          <h2 className="text-center mb-5">¿Por qué Octofit Tracker?</h2>
          <Col md={4} className="mb-4">
            <Card className="h-100 shadow-sm">
              <Card.Body>
                <h5 className="card-title">📊 Registra Actividades</h5>
                <p className="card-text">
                  Mantén un registro detallado de todas tus actividades físicas, 
                  calorías y tiempo invertido.
                </p>
              </Card.Body>
            </Card>
          </Col>
          <Col md={4} className="mb-4">
            <Card className="h-100 shadow-sm">
              <Card.Body>
                <h5 className="card-title">👥 Forma Equipos</h5>
                <p className="card-text">
                  Crea equipos con amigos y compite juntos en una emocionante 
                  clasificación semanal.
                </p>
              </Card.Body>
            </Card>
          </Col>
          <Col md={4} className="mb-4">
            <Card className="h-100 shadow-sm">
              <Card.Body>
                <h5 className="card-title">🎯 Obtén Recomendaciones</h5>
                <p className="card-text">
                  Recibe sugerencias de entrenamiento personalizadas basadas en 
                  tu nivel de fitness.
                </p>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}
    </Container>
  );
};

export default Home;
