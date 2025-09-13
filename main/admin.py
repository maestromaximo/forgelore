from django.contrib import admin
from .models import (
    Project, Paper, PaperSection, Literature, Citation,
    Hypothesis, Note, Simulation, Attachment,
    AutomationJob, AutomationTask
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('name', 'abstract', 'description', 'owner__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'content_format', 'created_at', 'updated_at')
    list_filter = ('content_format', 'created_at', 'updated_at')
    search_fields = ('title', 'abstract', 'content_raw', 'project__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)


@admin.register(PaperSection)
class PaperSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'paper', 'kind', 'order', 'created_at')
    list_filter = ('kind', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'paper__title')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('paper', 'order')


@admin.register(Literature)
class LiteratureAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'year', 'source_type', 'is_open_access', 'created_at')
    list_filter = ('source_type', 'is_open_access', 'year', 'created_at', 'published_date')
    search_fields = ('title', 'authors', 'journal_or_publisher', 'doi', 'arxiv_id', 'abstract', 'tags')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-year', 'title')


@admin.register(Citation)
class CitationAdmin(admin.ModelAdmin):
    list_display = ('paper', 'literature', 'section', 'style', 'order', 'created_at')
    list_filter = ('style', 'created_at', 'updated_at')
    search_fields = ('paper__title', 'literature__title', 'section__title', 'quote', 'note')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('paper', 'order')


@admin.register(Hypothesis)
class HypothesisAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'confidence', 'p_value', 'created_at')
    list_filter = ('status', 'created_at', 'updated_at', 'confidence')
    search_fields = ('title', 'statement', 'evaluation_summary', 'project__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'pinned', 'updated_at', 'created_at')
    list_filter = ('pinned', 'created_at', 'updated_at')
    search_fields = ('title', 'body', 'project__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-pinned', '-updated_at')


@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'hypothesis', 'language', 'status', 'started_at', 'finished_at')
    list_filter = ('language', 'status', 'created_at', 'started_at', 'finished_at')
    search_fields = ('name', 'description', 'code', 'stdout', 'stderr', 'project__name')
    readonly_fields = ('created_at', 'updated_at', 'started_at', 'finished_at', 'exit_code', 'stdout', 'stderr')
    ordering = ('-updated_at',)


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('label', 'kind', 'mime_type', 'content_object', 'created_at')
    list_filter = ('kind', 'created_at', 'updated_at')
    search_fields = ('label', 'text_content', 'mime_type')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)


@admin.register(AutomationJob)
class AutomationJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'status', 'started_at', 'finished_at', 'created_at')
    list_filter = ('status', 'created_at', 'started_at', 'finished_at')
    search_fields = ('project__name', 'message')
    readonly_fields = ('created_at', 'updated_at', 'started_at', 'finished_at')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('project')


@admin.register(AutomationTask)
class AutomationTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'job', 'status', 'progress', 'started_at', 'finished_at', 'created_at')
    list_filter = ('status', 'created_at', 'started_at', 'finished_at')
    search_fields = ('name', 'message', 'job__project__name')
    readonly_fields = ('created_at', 'updated_at', 'started_at', 'finished_at')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('job__project')
