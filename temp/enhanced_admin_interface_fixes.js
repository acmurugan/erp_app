// =============================================================================
// ENHANCED ADMIN INTERFACE FIXES - Better Column Reordering & Parameter Handling
// =============================================================================

// Enhanced Column Drag and Drop with Better Positioning
function enhanceColumnReordering() {
    const displayedContainer = document.getElementById('displayedColumns');
    
    if (displayedContainer) {
        // Make the container itself droppable
        displayedContainer.addEventListener('dragover', allowColumnDrop);
        displayedContainer.addEventListener('drop', handleColumnDropBetter);
        
        // Enhance existing column items
        const columnItems = displayedContainer.querySelectorAll('.column-item');
        columnItems.forEach(item => {
            makeColumnItemDraggableBetter(item);
        });
    }
}

// Better column item dragging
function makeColumnItemDraggableBetter(columnItem) {
    columnItem.draggable = true;
    columnItem.addEventListener('dragstart', handleColumnDragStartBetter);
    columnItem.addEventListener('dragend', handleColumnDragEndBetter);
    columnItem.addEventListener('dragover', handleColumnDragOverBetter);
    columnItem.addEventListener('drop', handleColumnDropOnItemBetter);
    
    // Add visual reordering buttons if not exists
    if (!columnItem.querySelector('.reorder-buttons')) {
        const reorderButtons = document.createElement('div');
        reorderButtons.className = 'reorder-buttons float-end me-2';
        reorderButtons.innerHTML = `
            <button class="btn btn-sm btn-outline-primary me-1" onclick="moveColumnUp(this)" title="Move Up">
                <i class="fas fa-arrow-up"></i>
            </button>
            <button class="btn btn-sm btn-outline-primary" onclick="moveColumnDown(this)" title="Move Down">
                <i class="fas fa-arrow-down"></i>
            </button>
        `;
        
        // Insert before existing buttons
        const existingButton = columnItem.querySelector('button');
        if (existingButton) {
            existingButton.parentNode.insertBefore(reorderButtons, existingButton);
        }
    }
}

// Enhanced drag handlers
let draggedColumnItem = null;
let dragOverItem = null;

function handleColumnDragStartBetter(e) {
    draggedColumnItem = this;
    this.style.opacity = '0.5';
    this.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
}

function handleColumnDragEndBetter(e) {
    this.style.opacity = '';
    this.classList.remove('dragging');
    
    // Remove all drag indicators
    document.querySelectorAll('.drag-indicator').forEach(el => el.remove());
    document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
    
    draggedColumnItem = null;
    dragOverItem = null;
}

function handleColumnDragOverBetter(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }
    
    if (draggedColumnItem && this !== draggedColumnItem) {
        e.dataTransfer.dropEffect = 'move';
        
        // Remove previous indicators
        document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
        
        // Add indicator
        this.classList.add('drag-over');
        dragOverItem = this;
        
        // Show visual drop indicator
        const rect = this.getBoundingClientRect();
        const midpoint = rect.top + rect.height / 2;
        
        if (e.clientY < midpoint) {
            this.style.borderTop = '2px solid #007bff';
            this.style.borderBottom = '';
        } else {
            this.style.borderBottom = '2px solid #007bff';
            this.style.borderTop = '';
        }
    }
    
    return false;
}

function handleColumnDropOnItemBetter(e) {
    if (e.stopPropagation) {
        e.stopPropagation();
    }
    
    if (draggedColumnItem && this !== draggedColumnItem) {
        const rect = this.getBoundingClientRect();
        const midpoint = rect.top + rect.height / 2;
        const insertBefore = e.clientY < midpoint;
        
        const container = this.parentNode;
        
        if (insertBefore) {
            container.insertBefore(draggedColumnItem, this);
        } else {
            container.insertBefore(draggedColumnItem, this.nextSibling);
        }
        
        // Update the configuration
        updateDisplayColumnOrderBetter();
    }
    
    // Clean up visual indicators
    this.style.borderTop = '';
    this.style.borderBottom = '';
    this.classList.remove('drag-over');
    
    return false;
}

function allowColumnDrop(e) {
    e.preventDefault();
    return false;
}

function handleColumnDropBetter(e) {
    e.preventDefault();
    
    if (draggedColumnItem) {
        // If dropped on empty space, append to end
        const container = e.currentTarget;
        container.appendChild(draggedColumnItem);
        updateDisplayColumnOrderBetter();
    }
    
    return false;
}

// Better column ordering update
function updateDisplayColumnOrderBetter() {
    const container = document.getElementById('displayedColumns');
    const columns = Array.from(container.children).map(item => {
        return item.getAttribute('data-column') || 
               item.textContent.replace(/^\s*[\u2630\u2631\u25B2\u25BC]?\s*/, '').replace(/\s*[×↑↓].*$/, '').trim();
    });
    
    console.log('Updated column order:', columns);
    
    if (currentReport && currentReport.rpt_params) {
        currentReport.rpt_params.display_columns = columns;
        updateJsonPreview();
        showSuccess('Column order updated');
    }
}

// Better move functions
function moveColumnUp(button) {
    const columnItem = button.closest('.column-item');
    const prevItem = columnItem.previousElementSibling;
    if (prevItem) {
        columnItem.parentNode.insertBefore(columnItem, prevItem);
        updateDisplayColumnOrderBetter();
    }
}

function moveColumnDown(button) {
    const columnItem = button.closest('.column-item');
    const nextItem = columnItem.nextElementSibling;
    if (nextItem) {
        columnItem.parentNode.insertBefore(nextItem, columnItem);
        updateDisplayColumnOrderBetter();
    }
}

// Enhanced addColumnToContainer with better reordering
function addColumnToContainerBetter(container, column, type) {
    const existing = Array.from(container.children).some(child => {
        const text = child.textContent || child.innerText;
        const existingColumn = text.replace(/^\s*[\u2630\u2631\u25B2\u25BC]?\s*/, '').replace(/\s*[×↑↓].*$/, '').trim();
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
        makeColumnItemDraggableBetter(columnDiv);
    }
    
    updateJsonPreview();
    
    if (type === 'displayed' && !document.querySelector(`input[data-column="${column}"]`)) {
        addColumnHeader(column);
    }
}

// Enhanced parameter form filtering with visibility support
function buildParameterFormWithVisibility(parameters) {
    const form = document.createElement('form');
    form.innerHTML = '';
    
    parameters.forEach(param => {
        // Only include visible parameters (default to true if not specified)
        if (param.visible !== false) {
            const formGroup = document.createElement('div');
            formGroup.className = 'mb-3';
            
            const label = document.createElement('label');
            label.className = 'form-label';
            label.textContent = param.name;
            if (param.required) {
                label.innerHTML += ' <span class="text-danger">*</span>';
            }
            
            let input;
            if (param.type === 'date') {
                input = document.createElement('input');
                input.type = 'text';
                input.className = 'form-control';
                input.placeholder = 'DD/MM/YYYY';
            } else if (param.type === 'select' && param.options) {
                input = document.createElement('select');
                input.className = 'form-control';
                param.options.forEach(option => {
                    const optionEl = document.createElement('option');
                    optionEl.value = option.value;
                    optionEl.textContent = option.text;
                    if (option.value === param.default) {
                        optionEl.selected = true;
                    }
                    input.appendChild(optionEl);
                });
            } else {
                input = document.createElement('input');
                input.type = 'text';
                input.className = 'form-control';
            }
            
            input.name = param.field;
            input.value = param.default || '';
            input.required = param.required;
            
            formGroup.appendChild(label);
            formGroup.appendChild(input);
            form.appendChild(formGroup);
        }
    });
    
    return form;
}

// Enhanced populateColumns with better error handling
function populateColumnsEnhanced() {
    const availableContainer = document.getElementById('availableColumns');
    if (!availableContainer) return;
    
    availableContainer.innerHTML = '';

    let columnsToShow = [];
    
    // Try to get available columns from current report
    if (currentReport && currentReport.rpt_params && currentReport.rpt_params.available_columns) {
        columnsToShow = currentReport.rpt_params.available_columns;
        console.log('Found available_columns in config:', columnsToShow.length);
    } else {
        console.log('No available_columns found in config');
    }

    if (columnsToShow && columnsToShow.length > 0) {
        columnsToShow.forEach(column => {
            const columnDiv = document.createElement('div');
            columnDiv.className = 'column-item available-column';
            columnDiv.draggable = true;
            columnDiv.ondragstart = (e) => drag(e, column);
            columnDiv.innerHTML = `
                <i class="fas fa-grip-vertical me-2"></i>${column}
            `;
            availableContainer.appendChild(columnDiv);
        });
        
        showInfo(`Loaded ${columnsToShow.length} available columns`);
    } else {
        availableContainer.innerHTML = `
            <div class="alert alert-warning">
                <i class="fas fa-exclamation-triangle me-2"></i>
                <strong>No Available Columns</strong><br>
                Run the SQL update script to populate available_columns for this report.
            </div>
        `;
    }
}

// Enhanced CSS for better visual feedback
const enhancedReorderingCSS = `
    <style>
    .column-item {
        position: relative;
        transition: all 0.3s ease;
        border: 1px solid #dee2e6;
        margin: 2px 0;
        padding: 8px;
        border-radius: 4px;
    }
    
    .column-item.dragging {
        opacity: 0.5;
        transform: scale(0.95);
    }
    
    .column-item.drag-over {
        background-color: #e7f3ff;
        border-color: #007bff;
    }
    
    .column-item:hover .reorder-buttons {
        opacity: 1;
    }
    
    .reorder-buttons {
        opacity: 0.6;
        transition: opacity 0.3s ease;
    }
    
    .drag-indicator {
        height: 2px;
        background-color: #007bff;
        margin: 2px 0;
        border-radius: 1px;
    }
    
    .parameter-item {
        transition: all 0.3s ease;
        cursor: move;
    }
    
    .parameter-hidden {
        opacity: 0.6;
        background-color: #f8f9fa;
        border-left: 3px solid #ffc107;
    }
    
    .parameter-visible {
        border-left: 3px solid #28a745;
    }
    
    .available-column {
        cursor: grab;
    }
    
    .available-column:hover {
        background-color: #f8f9fa;
    }
    </style>
`;

// Initialize all enhancements
function initializeEnhancedAdminInterface() {
    // Add enhanced CSS
    document.head.insertAdjacentHTML('beforeend', enhancedReorderingCSS);
    
    // Wait a bit for the page to load, then enhance
    setTimeout(() => {
        enhanceColumnReordering();
        
        // Override the original functions
        window.addColumnToContainer = addColumnToContainerBetter;
        window.populateColumns = populateColumnsEnhanced;
        
        console.log('Enhanced admin interface initialized');
        
        // If there's a current report, refresh the available columns
        if (currentReport) {
            populateColumnsEnhanced();
        }
    }, 1000);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeEnhancedAdminInterface);
} else {
    initializeEnhancedAdminInterface();
}