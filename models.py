from django.db import models

class ClienteSoporte(models.Model):
    # El id_cliente se genera automáticamente como Primary Key (id) a menos que se especifique otro.
    # Si necesitas que sea explícito: id_cliente = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=255)
    contacto_principal = models.CharField(max_length=100)
    email_contacto = models.EmailField(max_length=100)
    telefono_contacto = models.CharField(max_length=20)
    sector_empresa = models.CharField(max_length=100)
    fecha_registro = models.DateField()
    nivel_soporte = models.CharField(max_length=50)
    sitio_web = models.URLField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Cliente de Soporte"
        verbose_name_plural = "Clientes de Soporte"
        db_table = 'Cliente_Soporte'

    def __str__(self):
        return self.nombre_empresa


class AgenteSoporte(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=20)
    especialidad = models.CharField(max_length=100)
    fecha_contratacion = models.DateField()
    nivel_experiencia = models.CharField(max_length=50)
    turno = models.CharField(max_length=50)
    dni = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Agente de Soporte"
        verbose_name_plural = "Agentes de Soporte"
        db_table = 'Agente_Soporte'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class TicketSoporte(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50)
    prioridad = models.CharField(max_length=20)
    
    # Relación Muchos a Uno con Cliente
    cliente = models.ForeignKey(
        ClienteSoporte, 
        on_delete=models.CASCADE, 
        db_column='id_cliente',
        related_name='tickets'
    )
    
    # Relación Muchos a Uno con Agente
    agente_asignado = models.ForeignKey(
        AgenteSoporte, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        db_column='id_agente_asignado',
        related_name='tickets_asignados'
    )
    
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    tipo_incidente = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50)
    resolucion = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Ticket de Soporte"
        verbose_name_plural = "Tickets de Soporte"
        db_table = 'Ticket_Soporte'

    def __str__(self):
        return f"#{self.id} - {self.titulo}"


class Interaccion(models.Model):
    # Relación Muchos a Uno con Ticket
    ticket = models.ForeignKey(
        TicketSoporte, 
        on_delete=models.CASCADE, 
        db_column='id_ticket',
        related_name='interacciones'
    )
    
    # Relación Muchos a Uno con Agente
    agente = models.ForeignKey(
        AgenteSoporte, 
        on_delete=models.SET_NULL, 
        null=True, 
        db_column='id_agente'
    )
    
    fecha_interaccion = models.DateTimeField(auto_now_add=True)
    tipo_interaccion = models.CharField(max_length=50)
    descripcion_interaccion = models.TextField()
    # Se usa TextField para guardar rutas de archivos o JSON, ya que la especificación pedía TEXT
    archivos_adjuntos = models.TextField(null=True, blank=True) 
    duracion_minutos = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Interacción"
        verbose_name_plural = "Interacciones"
        db_table = 'Interaccion'

    def __str__(self):
        return f"Interacción {self.id} - Ticket {self.ticket_id}"


class BaseConocimiento(models.Model):
    titulo_articulo = models.CharField(max_length=255)
    contenido_articulo = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    autor = models.CharField(max_length=100)
    categoria_articulo = models.CharField(max_length=50)
    palabras_clave = models.TextField()
    veces_consultado = models.IntegerField(default=0)
    es_publico = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Artículo de Base de Conocimiento"
        verbose_name_plural = "Base de Conocimiento"
        db_table = 'Base_Conocimiento'

    def __str__(self):
        return self.titulo_articulo


class SatisfaccionCliente(models.Model):
    # Relación con Ticket (según esquema Muchos a Uno, aunque lógicamente suele ser Uno a Uno)
    ticket = models.ForeignKey(
        TicketSoporte, 
        on_delete=models.CASCADE, 
        db_column='id_ticket',
        related_name='encuestas_satisfaccion'
    )
    
    fecha_encuesta = models.DateTimeField(auto_now_add=True)
    calificacion_agente = models.IntegerField()
    calificacion_resolucion = models.IntegerField()
    comentarios_cliente = models.TextField(null=True, blank=True)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    fue_resuelto = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Satisfacción del Cliente"
        verbose_name_plural = "Satisfacción del Cliente"
        db_table = 'Satisfaccion_Cliente'

    def __str__(self):
        return f"Encuesta Ticket #{self.ticket_id}"


class SLA(models.Model):
    nombre_sla = models.CharField(max_length=100)
    descripcion = models.TextField()
    tiempo_respuesta_horas = models.IntegerField()
    tiempo_resolucion_horas = models.IntegerField()
    prioridad_asociada = models.CharField(max_length=20)
    penalizacion_incumplimiento = models.TextField(null=True, blank=True)
    es_activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Acuerdo de Nivel de Servicio (SLA)"
        verbose_name_plural = "SLAs"
        db_table = 'SLA'

    def __str__(self):
        return self.nombre_sla
