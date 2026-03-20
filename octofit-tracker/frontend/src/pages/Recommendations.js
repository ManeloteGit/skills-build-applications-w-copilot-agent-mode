import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Spinner, Alert, Badge, Form } from 'react-bootstrap';
import { recommendationService } from '../services/api';

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [filter, setFilter] = useState('active');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchRecommendations();
  }, [filter]);

  const fetchRecommendations = async () => {
    try {
      setError('');
      let response;
      
      switch(filter) {
        case 'pending':
          response = await recommendationService.getPending();
          break;
        case 'completed':
          response = await recommendationService.getCompleted();
          break;
        default:
          response = await recommendationService.getActive();
      }
      
      setRecommendations(response.data.results || response.data || []);
    } catch (err) {
      setError('Error al cargar las recomendaciones');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async (recId, action) => {
    try {
      setError('');
      
      switch(action) {
        case 'view':
          await recommendationService.viewRecommendation(recId);
          break;
        case 'accept':
          await recommendationService.acceptRecommendation(recId);
          break;
        case 'reject':
          await recommendationService.rejectRecommendation(recId);
          break;
        case 'complete':
          await recommendationService.completeRecommendation(recId);
          break;
        default:
          break;
      }
      
      setSuccess('Acción realizada correctamente');
      await fetchRecommendations();
    } catch (err) {
      setError('Error al realizar la acción');
      console.error(err);
    }
  };

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
      <Row className="mb-4">
        <Col>
          <h1 className="display-5 fw-bold">🎯 Mis Recomendaciones</h1>
        </Col>
      </Row>

      {error && <Alert variant="danger" onClose={() => setError('')} dismissible>{error}</Alert>}
      {success && <Alert variant="success" onClose={() => setSuccess('')} dismissible>{success}</Alert>}

      <Row className="mb-4">
        <Col>
          <Form.Group>
            <Form.Label className="fw-bold">Filtrar por:</Form.Label>
            <div className="d-flex gap-2">
              <Button 
                variant={filter === 'active' ? 'primary' : 'outline-primary'}
                onClick={() => setFilter('active')}
              >
                Activas
              </Button>
              <Button 
                variant={filter === 'pending' ? 'primary' : 'outline-primary'}
                onClick={() => setFilter('pending')}
              >
                Pendientes
              </Button>
              <Button 
                variant={filter === 'completed' ? 'primary' : 'outline-primary'}
                onClick={() => setFilter('completed')}
              >
                Completadas
              </Button>
            </div>
          </Form.Group>
        </Col>
      </Row>

      <Row>
        {recommendations.length === 0 ? (
          <Col>
            <Alert variant="info" className="text-center">
              No hay recomendaciones en esta categoría
            </Alert>
          </Col>
        ) : (
          recommendations.map(rec => (
            <Col md={6} className="mb-4" key={rec.id}>
              <Card className={`shadow-sm h-100 border-${
                rec.status === 'completed' ? 'success' :
                rec.status === 'pending' ? 'warning' : 'info'
              }`}>
                <Card.Header className={`bg-${
                  rec.status === 'completed' ? 'success' :
                  rec.status === 'pending' ? 'warning' : 'info'
                } text-white`}>
                  <div className="d-flex justify-content-between align-items-start">
                    <h5 className="mb-2">{rec.title}</h5>
                    <Badge bg={
                      rec.status === 'completed' ? 'success' :
                      rec.status === 'pending' ? 'warning' : 'info'
                    }>
                      {rec.status_display}
                    </Badge>
                  </div>
                </Card.Header>
                <Card.Body>
                  <p className="card-text mb-3">{rec.description}</p>
                  
                  <div className="mb-3">
                    <Badge bg="secondary" className="me-2">
                      {rec.recommendation_type_display}
                    </Badge>
                    {rec.intensity && (
                      <Badge bg="info" className="me-2">
                        Intensidad: {rec.intensity_display}
                      </Badge>
                    )}
                    {rec.estimated_duration_minutes && (
                      <Badge bg="light" text="dark">
                        ⏱️ {rec.estimated_duration_minutes} min
                      </Badge>
                    )}
                  </div>

                  <p className="small text-muted mb-0">
                    <strong>Razón:</strong> {rec.reason}
                  </p>
                </Card.Body>
                <Card.Footer className="bg-light">
                  <div className="d-flex gap-2">
                    {rec.status === 'pending' && (
                      <>
                        <Button 
                          variant="success" 
                          size="sm"
                          onClick={() => handleAction(rec.id, 'accept')}
                          className="flex-grow-1"
                        >
                          Aceptar
                        </Button>
                        <Button 
                          variant="danger" 
                          size="sm"
                          onClick={() => handleAction(rec.id, 'reject')}
                          className="flex-grow-1"
                        >
                          Rechazar
                        </Button>
                      </>
                    )}
                    {rec.status === 'accepted' && (
                      <Button 
                        variant="success" 
                        size="sm"
                        onClick={() => handleAction(rec.id, 'complete')}
                        className="w-100"
                      >
                        Marcar como Completada
                      </Button>
                    )}
                    {rec.status === 'viewed' && (
                      <>
                        <Button 
                          variant="primary" 
                          size="sm"
                          onClick={() => handleAction(rec.id, 'accept')}
                          className="flex-grow-1"
                        >
                          Aceptar
                        </Button>
                        <Button 
                          variant="outline-danger" 
                          size="sm"
                          onClick={() => handleAction(rec.id, 'reject')}
                          className="flex-grow-1"
                        >
                          Rechazar
                        </Button>
                      </>
                    )}
                  </div>
                </Card.Footer>
              </Card>
            </Col>
          ))
        )}
      </Row>
    </Container>
  );
};

export default Recommendations;
