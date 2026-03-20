import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Form, Alert, Spinner, ListGroup } from 'react-bootstrap';
import { teamService } from '../services/api';

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const [formData, setFormData] = useState({
    name: '',
    description: '',
  });

  useEffect(() => {
    fetchTeams();
  }, []);

  const fetchTeams = async () => {
    try {
      setError('');
      const response = await teamService.getTeams();
      setTeams(response.data.results || response.data || []);
    } catch (err) {
      setError('Error al cargar los equipos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      await teamService.createTeam(formData);
      setSuccess('Equipo creado correctamente');
      setShowForm(false);
      setFormData({ name: '', description: '' });
      await fetchTeams();
    } catch (err) {
      setError('Error al crear el equipo');
      console.error(err);
    }
  };

  const handleDeleteTeam = async (teamId) => {
    if (window.confirm('¿Deseas eliminar este equipo?')) {
      try {
        await teamService.deleteTeam(teamId);
        setSuccess('Equipo eliminado correctamente');
        await fetchTeams();
      } catch (err) {
        setError('Error al eliminar el equipo');
      }
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
          <h1 className="display-5 fw-bold">👥 Mis Equipos</h1>
        </Col>
        <Col className="text-end">
          <Button 
            variant={showForm ? 'secondary' : 'success'}
            onClick={() => setShowForm(!showForm)}
          >
            {showForm ? 'Cancelar' : '➕ Crear Equipo'}
          </Button>
        </Col>
      </Row>

      {error && <Alert variant="danger" onClose={() => setError('')} dismissible>{error}</Alert>}
      {success && <Alert variant="success" onClose={() => setSuccess('')} dismissible>{success}</Alert>}

      {showForm && (
        <Card className="mb-4 shadow-sm">
          <Card.Header className="bg-success text-white">
            <h5 className="mb-0">Crear Nuevo Equipo</h5>
          </Card.Header>
          <Card.Body>
            <Form onSubmit={handleSubmit}>
              <Form.Group className="mb-3">
                <Form.Label>Nombre del Equipo</Form.Label>
                <Form.Control
                  type="text"
                  name="name"
                  placeholder="Ej: Team Fitness 2024"
                  value={formData.name}
                  onChange={handleChange}
                  required
                />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Descripción</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={3}
                  name="description"
                  placeholder="Describe tu equipo"
                  value={formData.description}
                  onChange={handleChange}
                />
              </Form.Group>

              <Button variant="success" type="submit" className="w-100">
                Crear Equipo
              </Button>
            </Form>
          </Card.Body>
        </Card>
      )}

      <Row>
        {teams.length === 0 ? (
          <Col>
            <Alert variant="info" className="text-center">
              No tienes equipos aún. ¡Crea uno ahora para comenzar a competir!
            </Alert>
          </Col>
        ) : (
          teams.map(team => (
            <Col md={6} className="mb-4" key={team.id}>
              <Card className="shadow-sm h-100">
                <Card.Header className="bg-primary text-white">
                  <h5 className="mb-0">{team.name}</h5>
                </Card.Header>
                <Card.Body>
                  <p className="text-muted mb-3">{team.description || 'Sin descripción'}</p>
                  <ListGroup variant="flush" className="mb-3">
                    <ListGroup.Item>
                      <strong>Líder:</strong> {team.leader_username}
                    </ListGroup.Item>
                    <ListGroup.Item>
                      <strong>Miembros:</strong> {team.actual_member_count || 0}
                    </ListGroup.Item>
                  </ListGroup>
                </Card.Body>
                <Card.Footer className="bg-light">
                  <div className="d-flex gap-2">
                    <Button variant="outline-primary" size="sm" className="flex-grow-1">
                      Ver Detalles
                    </Button>
                    <Button 
                      variant="outline-danger" 
                      size="sm"
                      onClick={() => handleDeleteTeam(team.id)}
                    >
                      Eliminar
                    </Button>
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

export default Teams;
