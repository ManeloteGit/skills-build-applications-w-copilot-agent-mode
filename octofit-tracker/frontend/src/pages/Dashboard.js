import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Spinner, Alert, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { activityService, recommendationService } from '../services/api';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        setError('');
        const [statsRes, recsRes] = await Promise.all([
          activityService.getStatistics(),
          recommendationService.getActive(),
        ]);
        setStats(statsRes.data);
        setRecommendations(recsRes.data.results || recsRes.data || []);
      } catch (err) {
        setError('Error al cargar los datos del dashboard');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <Container className="d-flex justify-content-center align-items-center" style={{ minHeight: '70vh' }}>
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Cargando...</span>
        </Spinner>
      </Container>
    );
  }

  return (
    <Container>
      <Row className="mb-5">
        <Col>
          <h1 className="display-5 fw-bold">Bienvenido, {user?.first_name || user?.username}! 👋</h1>
        </Col>
      </Row>

      {error && <Alert variant="danger">{error}</Alert>}

      <Row className="mb-4">
        <Col md={3} className="mb-3">
          <Card className="text-center shadow-sm">
            <Card.Body>
              <h6 className="text-muted">Actividades</h6>
              <h2 className="mb-0">{stats?.total_activities || 0}</h2>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3} className="mb-3">
          <Card className="text-center shadow-sm">
            <Card.Body>
              <h6 className="text-muted">Minutos</h6>
              <h2 className="mb-0">{stats?.total_duration_minutes || 0}</h2>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3} className="mb-3">
          <Card className="text-center shadow-sm">
            <Card.Body>
              <h6 className="text-muted">Calorías</h6>
              <h2 className="mb-0">{stats?.total_calories_burned || 0}</h2>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3} className="mb-3">
          <Card className="text-center shadow-sm">
            <Card.Body>
              <h6 className="text-muted">Distancia (km)</h6>
              <h2 className="mb-0">{(stats?.total_distance_km || 0).toFixed(1)}</h2>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="mb-4">
        <Col md={6}>
          <Card className="shadow-sm">
            <Card.Header className="bg-primary text-white">
              <h5 className="mb-0">📋 Recomendaciones Activas</h5>
            </Card.Header>
            <Card.Body>
              {recommendations.length === 0 ? (
                <p className="text-muted">No hay recomendaciones activas en este momento.</p>
              ) : (
                <div>
                  {recommendations.slice(0, 3).map(rec => (
                    <div key={rec.id} className="mb-3 pb-3 border-bottom">
                      <h6 className="mb-1">{rec.title}</h6>
                      <p className="small text-muted mb-2">{rec.description}</p>
                      <div className="small">
                        <span className="badge bg-info me-2">{rec.recommendation_type_display}</span>
                        <span className="badge bg-secondary">{rec.intensity_display || 'Media'}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
              <Link to="/recommendations" className="btn btn-sm btn-primary mt-3">
                Ver todas las recomendaciones
              </Link>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card className="shadow-sm">
            <Card.Header className="bg-success text-white">
              <h5 className="mb-0">⚡ Acciones Rápidas</h5>
            </Card.Header>
            <Card.Body>
              <div className="d-grid gap-2">
                <Link to="/activities/new" className="btn btn-success">
                  ➕ Registrar Actividad
                </Link>
                <Link to="/profile" className="btn btn-outline-primary">
                  👤 Actualizar Perfil
                </Link>
                <Link to="/teams" className="btn btn-outline-primary">
                  👥 Mis Equipos
                </Link>
                <Link to="/leaderboard" className="btn btn-outline-primary">
                  🏆 Ver Clasificación
                </Link>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Dashboard;
