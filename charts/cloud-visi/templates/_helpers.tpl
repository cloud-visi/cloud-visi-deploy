{{- define "cloud-visi.name" -}}
{{- default .Release.Name .Values.fullnameOverride | trunc 54 | trimSuffix "-" -}}
{{- end -}}
{{- define "cloud-visi.labels" -}}
app.kubernetes.io/name: cloud-visi
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | quote }}
{{- end -}}
{{- define "cloud-visi.image" -}}
{{- if .Values.image.digest -}}
{{ printf "%s@%s" .Values.image.repository .Values.image.digest }}
{{- else -}}
{{ printf "%s:%s" .Values.image.repository (default .Chart.AppVersion .Values.image.tag) }}
{{- end -}}
{{- end -}}
