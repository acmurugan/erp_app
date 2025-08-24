// =============================================================================
// ENHANCED ADMIN INTERFACE - PARAMETER MANAGEMENT WITH DRAG/DROP AND CHECKBOXES
// =============================================================================

// Enhanced parameter management with drag/drop reordering and checkbox visibility
function addParameterToDOM(param, index) {
    const container = document.getElementById('parametersContainer');
    const paramDiv = document.createElement('div');
    paramDiv.className = 'card mb-2 parameter-item';
    paramDiv.draggable = true;
    paramDiv.setAttribute('data-param-index', index);
    
    // Add drag/drop event handlers
    paramDiv.addEventListener('dragstart', handleParameterDragStart);
    paramDiv.addEventListener('dragover', handleParameterDragOver);
    paramDiv.addEventListener('drop', handleParameterDrop);
    paramDiv.addEventListener('dragend', handleParameterDragEnd);
    
    paramDiv.innerHTML = `
        <div class="card-body">
            <div class="row align-items-center">
                <div class="col-md-1">
                    <div class="form-check">
                        <input class="form-check-input parameter-visible" type="checkbox" 
                               ${param.visible !== false ? 'checked' : ''} 
                               onchange="toggleParameterVisibility(${index}, this.checked)"
                               data-param-index="${index}">
                    </div>
                    <div class="drag-handle text-muted mt-1">
                        <i class="fas fa-grip-vertical"></i>
                    </div>
                </div>
                <div class="col-md-3">
                    <strong>${param.name}</strong><br>
                    <small class="text-muted">Field: ${param.field}</small>
                </div>
                <div class="col-md-2">
                    <span class="badge bg-secondary">${param.type}</span>
                </div>
                <div class="col-md-2">
                    Default: ${param.default || 'None'}
                </div>
                <div class="col-md-2">
                    ${param.required ? '<span class="badge bg-warning">Required</span>' : '<span class="badge bg-light text-dark">Optional</span>'}
                </div>
                <div class="col-md-2">
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="editParameterInline(${index})" title="Edit Parameter">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteParameter(${index})" title="Remove Parameter">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            <!-- Inline edit form (initially hidden) -->
            <div class="row mt-3 parameter-edit-form" id="paramEditForm${index}" style="display: none;">
                <div class="col-md-12">
                    <div class="border p-3 bg-light">
                        <div class="row">
                            <div class="col-md-3">
                                <label class="form-label">Parameter Name</label>
                                <input type="text" class="form-control form-control-sm" 
                                       id="paramName${index}" value="${param.name}">
                            </div>
                            <div class="col-md-3">
                                <label class="form-label">Field Name</label>
                                <input type="text" class="form-control form-control-sm" 
                                       id="paramField${index}" value="${param.field}">
                            </div>
                            <div class="col-md-2">
                                <label class="form-label">Type</label>
                                <select class="form-control form-control-sm" id="paramType${index}">
                                    <option value="text" ${param.type === 'text' ? 'selected' : ''}>Text</option>
                                    <option value="date" ${param.type === 'date' ? 'selected' : ''}>Date</option>
                                    <option value="number" ${param.type === 'number' ? 'selected' : ''}>Number</option>
                                    <option value="select" ${param.type === 'select' ? 'selected' : ''}>Select</option>
                                </select>
                            </div>
                            <div class="col-md-2">
                                <label class="form-label">Default Value</label>
                                <input type="text" class="form-control form-control-sm" 
                                       id="paramDefault${index}" value="${param.default || ''}">
                            </div>
                            <div class="col-md-2">
                                <div class="form-check mt-4">
                                    <input class="form-check-input" type="checkbox" 
                                           id="paramRequired${index}" ${param.required ? 'checked' : ''}>
                                    <label class="form-check-label" for="paramRequired${index}">Required</label>
                                </div>
                            </div>
                        </div>
                        <div class="row mt-2">
                            <div class="col-md-12 text-end">
                                <button class="btn btn-sm btn-success me-1" onclick="saveParameterInline(${index})">
                                    <i class="fas fa-check"></i> Save
                                </button>
                                <button class="btn btn-sm btn-secondary" onclick="cancelParameterEdit(${index})">
                                    <i class="fas fa-times"></i> Cancel
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    container.appendChild(paramDiv);
}

// Parameter drag and drop handlers
let draggedParameterElement = null;

function handleParameterDragStart(e) {
    draggedParameterElement = this;
    this.style.opacity = '0.5';
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.outerHTML);
}

function handleParameterDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }
    e.dataTransfer.dropEffect = 'move';
    this.classList.add('drag-over');
    return false;
}

function handleParameterDrop(e) {
    if (e.stopPropagation) {
        e.stopPropagation();
    }
    
    if (draggedParameterElement !== this) {
        const container = document.getElementById('parametersContainer');
        const allItems = Array.from(container.children);
        const draggedIndex = allItems.indexOf(draggedParameterElement);
        const targetIndex = allItems.indexOf(this);
        
        if (draggedIndex < targetIndex) {
            this.parentNode.insertBefore(draggedParameterElement, this.nextSibling);
        } else {
            this.parentNode.insertBefore(draggedParameterElement, this);
        }
        
        // Update parameter order and rebuild with new indices
        reorderParameters();
    }
    
    this.classList.remove('drag-over');
    return false;
}

function handleParameterDragEnd(e) {
    this.style.opacity = '';
    this.classList.remove('drag-over');
    
    // Clean up any remaining drag-over classes
    const allItems = document.querySelectorAll('.parameter-item');
    allItems.forEach(item => item.classList.remove('drag-over'));
}

// Reorder parameters based on DOM order
function reorderParameters() {
    const container = document.getElementById('parametersContainer');
    const items = Array.from(container.children);
    
    // Rebuild the parameters array in the new order
    const newParameters = [];
    items.forEach((item, newIndex) => {
        const oldIndex = parseInt(item.getAttribute('data-param-index'));
        const param = currentReport.rpt_params.parameters[oldIndex];
        if (param) {
            newParameters.push(param);
        }
    });
    
    // Update the current report parameters
    currentReport.rpt_params.parameters = newParameters;
    
    // Rebuild the parameter display with new indices
    populateParameters(newParameters);
    updateJsonPreview();
}

// Toggle parameter visibility
function toggleParameterVisibility(index, isVisible) {
    if (currentReport && currentReport.rpt_params && currentReport.rpt_params.parameters) {
        // Update the parameter object
        currentReport.rpt_params.parameters[index].visible = isVisible;
        
        // Visual feedback
        const paramDiv = document.querySelector(`[data-param-index="${index}"]`);
        if (paramDiv) {
            if (isVisible) {
                paramDiv.classList.remove('parameter-hidden');
                paramDiv.style.opacity = '1';
            } else {
                paramDiv.classList.add('parameter-hidden');
                paramDiv.style.opacity = '0.6';
            }
        }
        
        updateJsonPreview();
    }
}

// Inline parameter editing functions
function editParameterInline(index) {
    const editForm = document.getElementById(`paramEditForm${index}`);
    if (editForm) {
        editForm.style.display = editForm.style.display === 'none' ? 'block' : 'none';
    }
}

function saveParameterInline(index) {
    const param = currentReport.rpt_params.parameters[index];
    if (param) {
        // Get values from form
        param.name = document.getElementById(`paramName${index}`).value;
        param.field = document.getElementById(`paramField${index}`).value;
        param.type = document.getElementById(`paramType${index}`).value;
        param.default = document.getElementById(`paramDefault${index}`).value;
        param.required = document.getElementById(`paramRequired${index}`).checked;
        
        // Hide edit form and refresh display
        document.getElementById(`paramEditForm${index}`).style.display = 'none';
        populateParameters(currentReport.rpt_params.parameters);
        updateJsonPreview();
        showSuccess('Parameter updated successfully');
    }
}

function cancelParameterEdit(index) {
    document.getElementById(`paramEditForm${index}`).style.display = 'none';
}

// Enhanced column ordering for display columns
function makeColumnsSortable() {
    const displayedContainer = document.getElementById('displayedColumns');
    if (displayedContainer) {
        // Add sortable functionality to displayed columns
        displayedContainer.addEventListener('dragover', handleColumnDragOver);
        displayedContainer.addEventListener('drop', handleColumnDrop);
        
        // Make existing column items sortable
        const columnItems = displayedContainer.querySelectorAll('.column-item');
        columnItems.forEach(item => {
            makeColumnItemSortable(item);
        });
    }
}

function makeColumnItemSortable(columnItem) {
    columnItem.draggable = true;
    columnItem.addEventListener('dragstart', handleColumnDragStart);
    columnItem.addEventListener('dragend', handleColumnDragEnd);
    
    // Add up/down buttons for reordering
    if (!columnItem.querySelector('.order-buttons')) {
        const orderButtons = document.createElement('div');
        orderButtons.className = 'order-buttons float-end me-2';
        orderButtons.innerHTML = `
            <button class="btn btn-sm btn-outline-secondary me-1" onclick="moveColumnUp(this)" title="Move Up">
                <i class="fas fa-arrow-up"></i>
            </button>
            <button class="btn btn-sm btn-outline-secondary" onclick="moveColumnDown(this)" title="Move Down">
                <i class="fas fa-arrow-down"></i>
            </button>
        `;
        
        // Insert before the remove button
        const removeButton = columnItem.querySelector('button');
        if (removeButton) {
            removeButton.parentNode.insertBefore(orderButtons, removeButton);
        }
    }
}

// Column drag handlers for ordering
let draggedColumnElement = null;

function handleColumnDragStart(e) {
    draggedColumnElement = this;
    this.style.opacity = '0.5';
}

function handleColumnDragEnd(e) {
    this.style.opacity = '';
    draggedColumnElement = null;
}

function handleColumnDragOver(e) {
    e.preventDefault();
    return false;
}

function handleColumnDrop(e) {
    e.preventDefault();
    
    if (draggedColumnElement && e.target !== draggedColumnElement) {
        const container = e.currentTarget;
        const items = Array.from(container.children);
        const draggedIndex = items.indexOf(draggedColumnElement);
        const targetIndex = items.indexOf(e.target.closest('.column-item'));
        
        if (targetIndex >= 0 && draggedIndex !== targetIndex) {
            if (draggedIndex < targetIndex) {
                container.insertBefore(draggedColumnElement, items[targetIndex].nextSibling);
            } else {
                container.insertBefore(draggedColumnElement, items[targetIndex]);
            }
            
            updateDisplayColumnOrder();
        }
    }
    
    return false;
}

// Move column up/down with buttons
function moveColumnUp(button) {
    const columnItem = button.closest('.column-item');
    const prevItem = columnItem.previousElementSibling;
    if (prevItem) {
        columnItem.parentNode.insertBefore(columnItem, prevItem);
        updateDisplayColumnOrder();
    }
}

function moveColumnDown(button) {
    const columnItem = button.closest('.column-item');
    const nextItem = columnItem.nextElementSibling;
    if (nextItem) {
        columnItem.parentNode.insertBefore(nextItem, columnItem);
        updateDisplayColumnOrder();
    }
}

// Update display column order in configuration
function updateDisplayColumnOrder() {
    const container = document.getElementById('displayedColumns');
    const columns = Array.from(container.children).map(item => {
        return item.getAttribute('data-column') || 
               item.textContent.replace(/^\s*[\u2630\u2631]?\s*/, '').replace(/\s*×?\s*$/, '').trim();
    });
    
    if (currentReport && currentReport.rpt_params) {
        currentReport.rpt_params.display_columns = columns;
        updateJsonPreview();
    }
}

// Enhanced populateColumns function that loads available columns from config
function populateColumns(columns) {
    const availableContainer = document.getElementById('availableColumns');
    availableContainer.innerHTML = '';

    // Use available_columns from config if present, otherwise use provided columns
    let columnsToShow = columns;
    if (currentReport && currentReport.rpt_params && currentReport.rpt_params.available_columns) {
        columnsToShow = currentReport.rpt_params.available_columns;
    }

    if (columnsToShow && columnsToShow.length > 0) {
        columnsToShow.forEach(column => {
            const columnDiv = document.createElement('div');
            columnDiv.className = 'column-item';
            columnDiv.draggable = true;
            columnDiv.ondragstart = (e) => drag(e, column);
            columnDiv.innerHTML = `
                <i class="fas fa-grip-vertical me-2"></i>${column}
            `;
            availableContainer.appendChild(columnDiv);
        });
    } else {
        availableContainer.innerHTML = '<p class="text-muted">No available columns configured for this report</p>';
    }
}

// Enhanced addColumnToContainer with sortable functionality
function addColumnToContainerEnhanced(container, column, type) {
    const existing = Array.from(container.children).some(child => {
        const text = child.textContent || child.innerText;
        const existingColumn = text.replace(/^\s*[\u2630\u2631]?\s*/, '').replace(/\s*×?\s*$/, '').trim();
        return existingColumn === column;
    });
    
    if (existing) {
        console.log(`Column ${column} already exists in container, skipping`);
        return;
    }

    const columnDiv = document.createElement('div');
    columnDiv.className = `column-item column-${type}`;
    columnDiv.setAttribute('data-column', column);
    columnDiv.innerHTML = `
        <i class="fas fa-grip-vertical me-2"></i>${column}
        <button class="btn btn-sm btn-outline-secondary float-end" onclick="removeFromContainer(this)">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    container.appendChild(columnDiv);
    
    // Make sortable if it's in displayed columns
    if (type === 'displayed') {
        makeColumnItemSortable(columnDiv);
    }
    
    updateJsonPreview();
    
    if (type === 'displayed' && !document.querySelector(`input[data-column="${column}"]`)) {
        addColumnHeader(column);
    }
}

// CSS styles for enhanced functionality
const enhancedStyles = `
    <style>
    .parameter-item {
        transition: opacity 0.3s ease;
        cursor: move;
    }
    
    .parameter-hidden {
        opacity: 0.6;
        background-color: #f8f9fa;
    }
    
    .drag-handle {
        cursor: move;
        text-align: center;
    }
    
    .drag-over {
        background-color: #e9ecef;
        border: 2px dashed #007bff;
    }
    
    .parameter-edit-form {
        border-top: 1px solid #dee2e6;
        margin-top: 10px;
        padding-top: 10px;
    }
    
    .column-item {
        position: relative;
        transition: all 0.3s ease;
    }
    
    .column-item:hover .order-buttons {
        opacity: 1;
    }
    
    .order-buttons {
        opacity: 0.6;
        transition: opacity 0.3s ease;
    }
    
    .form-check-input:checked {
        background-color: #28a745;
        border-color: #28a745;
    }
    </style>
`;

// Initialize enhanced functionality when document is ready
document.addEventListener('DOMContentLoaded', function() {
    // Add enhanced styles
    document.head.insertAdjacentHTML('beforeend', enhancedStyles);
    
    // Initialize sortable columns
    setTimeout(() => {
        makeColumnsSortable();
    }, 500);
});

// Override the original addColumnToContainer function
window.addColumnToContainer = addColumnToContainerEnhanced;