"""
Feature: Migrar Datos a RinoTime
Responsabilidad: Migrar asistencias a la base de datos RinoTime (biotimedb)
"""
from .routes.migrar_datos_routes import migrar_datos_bp

__all__ = ['migrar_datos_bp']
