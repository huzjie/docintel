{{- define "docintel.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "docintel.fullname" -}}
{{- default .Release.Name .Values.nameOverride }}
{{- end }}
