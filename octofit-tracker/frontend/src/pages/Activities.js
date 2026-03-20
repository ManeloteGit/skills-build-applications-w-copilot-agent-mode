import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Form, Alert, Spinner, Table } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { activityService } from '../services/api';

const Activities = () => {
  const [activities, setActivities] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    activity_type: 'running',
    name: '',
    duration_minutes: '',
    distance_km: '',
    calories_burned: '',
    intensity_level: 'medium',
    notes: '',
    performed_at: new Date().toISOString().slice(0, 16),
  });

  useEffect(() => {
    fetchActivities();
  }, []);

  const fetchActivities = async () => {
    try {
      setError('');
      const response = await activityService.getActivities({ ordering: '-performed_at' });
      setActivities(response.data.results || response.data || []);
    } catch (err) {
      setError('Error al cargar las actividades');
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
      const data = {
        ...formData,
        performed_at: new Date(formData.performed_at).toISOString(),
      };
      await activityService.createActivity(data);
      setSuccess('Actividad registrada correctamente');
      setShowForm(false);
      setFormData({
        activity_type: 'running',
        name: '',
        duration_minutes: '',
        distance_km: '',
        calories_burned: '',
        intensity_level: 'medium',
        notes: '',
        performed_at: new Date().toISOString().slice(0, 16),
      });
      await fetchActivities();
    } catch (err) {
      setError('Error al registrar la actividad');
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Deseas eliminar esta actividad?')) {
      try {
        await activityService.deleteActivity(id);
        setSuccess('Actividad eliminada correctamente');
        await fetchActivities();
      } catch (err) {
        setError('Error al eliminar la actividad');
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
          <h1 className="display-5 fw-bold">📊 Mis Actividades</h1>
        </Col>
        <Col className="text-end">
          <Button 
            variant={showForm ? 'secondary' : 'success'}
            onClick={() => setShowForm(!showForm)}
          >
            {showForm ? 'Cancelar' : '➕ Nueva Actividad'}
          </Button>
        </Col>
      </Row>

      {error && <Alert variant="danger" onClose={() => setError('')} dismissible>{error}</Alert>}
      {success && <Alert variant="success" onClose={() => setSuccess('')} dismissible>{success}</Alert>}

      {showForm && (
        <Card className="mb-4 shadow-sm">
          <Card.Header className="bg-success text-white">
            <h5 className="mb-0">Registrar Nueva Actividad</h5>
          </Card.Header>
          <Card.Body>
            <Form onSubmit={handleSubmit}>
              <Row>
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Tipo de Actividad</Form.Label>
                    <Form.Select
                      name="activity_type"
                      value={formData.activity_type}
                      onChange={handleChange}
                      required
                    >
                      <option value="running">Correr</option>
                      <option value="walking">Caminar</option>
                      <option value="cycling">Ciclismo</option>
                      <option value="swimming">Natación</option>
                      <option value="gym">Gimnasio</option>
                      <option value="yoga">Yoga</option>
                      <option value="sports">Deportes</option>
                      <option value="other">Otro</option>
                    </Form.Select>
                  </Form.Group>
                </Col>
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Nombre de la Actividad</Form.Label>
                    <Form.Control
                      type="text"
                      name="name"
                      placeholder="Ej: Carrera matutina"
                      value={formData.name}
                      onChange={handleChange}
                      required
                    />
                  </Form.Group>
                </Col>
              </Row>

              <Row>
                <Col md={3}>
                  <Form.Group className="mb-3">
                    <Form.Label>Duración (minutos)</Form.Label>
                    <Form.Control
                      type="number"
                      name="duration_minutes"
                      value={formData.duration_minutes}
                      onChange={handleChange}
                      required
                    />
                  </Form.Group>
                </Col>
                <Col md={3}>
                  <Form.Group className="mb-3">
                    <Form.Label>Distancia (km)</Form.Label>
                    <Form.Control
                      type="number"
                      step="0.1"
                      name="distance_km"
                      value={formData.distance_km}
                      onChange={handleChange}
                    />
                  </Form.Group>
                </Col>
                <Col md={3}>
                  <Form.Group className="mb-3">
                    <Form.Label>Calorías</Form.Label>
                    <Form.Control
                      type="number"
                      name="calories_burned"
                      value={formData.calories_burned}
                      onChange={handleChange}
                    />
                  </Form.Group>
                </Col>
                <Col md={3}>
                  <Form.Group className="mb-3">
                    <Form.Label>Intensidad</Form.Label>
                    <Form.Select
                      name="intensity_level"
                      value={formData.intensity_level}
                      onChange={handleChange}
                    >
                      <option value="low">Baja</option>
                      <option value="medium">Media</option>
                      <option value="high">Alta</option>
                      <option value="very_high">Muy Alta</option>
                    </Form.Select>
                  </Form.Group>
                </Col>
              </Row>

              <Row>
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Fecha y Hora</Form.Label>
                    <Form.Control
                      type="datetime-local"
                      name="performed_at"
                      value={formData.performed_at}
                      onChange={handleChange}
                      required
                    />
                  </Form.Group>
                </Col>
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Notas</Form.Label>
                    <Form.Control
                      as="textarea"
                      rows={1}
                      name="notes"
                      placeholder="Agrega notas sobre tu actividad"
                      value={formData.notes}
                      onChange={handleChange}
                    />
                  </Form.Group>
                </Col>
              </Row>

              <Button variant="success" type="submit" className="w-100">
                Guardar Actividad
              </Button>
            </Form>
          </Card.Body>
        </Card>
      )}

      <Card className="shadow-sm">
        <Card.Header className="bg-primary text-white">
          <h5 className="mb-0">Historial de Actividades</h5>
        </Card.Header>
        <Card.Body className="p-0">
          {activities.length === 0 ? (
            <div className="p-4 text-center text-muted">
              No tienes actividades registradas aún. ¡Comienza a registrar tus actividades!
            </div>
          ) : (
            <Table hover responsive className="mb-0">
              <thead className="table-light">
                <tr>
                  <th>Fecha</th>
                  <th>Actividad</th>
                  <th>Duración</th>
                  <th>Distancia</th>
                  <th>Calorías</th>
                  <th>Intensidad</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {activities.map(activity => (
                  <tr key={activity.id}>
                    <td>{new Date(activity.performed_at).toLocaleDateString('es-MX')}</td>
                    <td>
                      <strong>{activity.name}</strong>
                      <br />
                      <small className="text-muted">{activity.activity_type_display}</small>
                    </td>
                    <td>{activity.duration_minutes} min</td>
                    <td>{activity.distance_km ? `${activity.distance_km} km` : '-'}</td>
                    <td>{activity.calories_burned || '-'}</td>
                    <td>
                      <span className={`badge bg-${
                        activity.intensity_level === 'high' ? 'danger' :
                        activity.intensity_level === 'medium' ? 'warning' : 'success'
                      }`}>
                        {activity.intensity_level?.toUpperCase() || 'N/A'}
                      </span>
                    </td>
                    <td>
                      <Button
                        variant="danger"
                        size="sm"
                        onClick={() => handleDelete(activity.id)}
                      >
                        Eliminar
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          )}
        </Card.Body>
      </Card>
    </Container>
  );
};

export default Activities;
